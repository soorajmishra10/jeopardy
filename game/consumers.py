import asyncio
import json
from django.contrib.auth import get_user_model
from game.models import *
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core import serializers
import time

User = get_user_model()

class GameConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connected", event)
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.username = self.scope['user']
        self.room_size = await self.get_room_size(self.room_code)
        self.user_id = await self.get_user_id(self.room_code, self.username)
        print(self.username, self.room_code)

        u = await self.get_user(self.username)
        print(u, u.username, u.first_name)
        await self.set_online(self.room_code, self.username)

        room_users_dict = await self.get_online_users(self.room_code)
        
        await self.channel_layer.group_add(
            self.room_code,
            self.channel_name
        )

        await self.send({
            "type" : "websocket.accept"
        })

        my_response = {
            "message" : "onlineUsersList",
            "room_users_dict" : room_users_dict
        }

        await self.channel_layer.group_send(
            self.room_code,
            {
                "type" : "group_msg",
                "text" : json.dumps(my_response)
            }
        )

    async def group_msg(self, event):
        await self.send({
            "type" : "websocket.send",
            "text" : event['text']
        })

    async def websocket_receive(self, event):
        print("receive", event)
        received_data = event.get('text', None)
        if received_data is not None:
            loaded_data = json.loads(received_data)
            message = loaded_data.get('message')
            if message == "gameStartMessage":
                room_users_dict = await self.get_online_users(self.room_code)
                await self.set_game_started(self.room_code)
                turn = await self.get_turn(self.room_code)
                turn = (turn+1)%(self.room_size)
                
                questions = await self.get_questions()

                await self.set_turn(self.room_code, turn)
                # set_questions() method call
                q_count = loaded_data.get('q_count')
                my_response = {
                    "message" : "gameStartedMessage",
                    "room_users_dict" : room_users_dict,
                    "turn" : turn,
                    "questions" : questions,
                    "q_count" : q_count
                }

                await self.channel_layer.group_send(
                    self.room_code,
                    {
                        "type" : "group_msg",
                        "text" : json.dumps(my_response)
                    }
                )
            elif message == "nextQuestionRequestMsg":
                room_users_dict = await self.get_online_users(self.room_code)
                turn = await self.get_turn(self.room_code)
                start_time = round(time.time()*1000)
                q_count = int(loaded_data.get('q_count'))+1
                await self.set_is_round_over(self.room_code, False)
                my_response = {
                    "message" : "nextQuestionReplyMsg",
                    "room_users_dict" : room_users_dict,
                    "q_category" : loaded_data.get('q_category'),
                    "q_points" : loaded_data.get('q_points'),
                    "q_index" : loaded_data.get('q_index'),
                    "q_count" : q_count,
                    "turn" : turn,
                    "start_time" : str(start_time).strip("L") 
                }

                await self.channel_layer.group_send(
                    self.room_code,
                    {
                        "type" : "group_msg",
                        "text" : json.dumps(my_response)
                    }
                )
            elif message == "answerMessage":
                cur_time = round(time.time()*1000)
                start_time = int(loaded_data.get('timestamp'))
                if cur_time < start_time+60000:
                    question_no = loaded_data.get('q_id')
                    
                    correct_ans = await self.get_correct_answer(question_no)
                    received_ans = loaded_data.get('q_ans')
                    received_ans = received_ans.upper()

                    if received_ans == correct_ans:
                        q_points = int(loaded_data.get('q_pnt'))
                        await self.update_score(self.room_code, self.username, q_points)
                        room_users_dict = await self.get_online_users(self.room_code)

                        room_users_obj_list = room_users_dict['room_users']
                        room_users_list = []
                        for i in range(len(room_users_obj_list)):
                            room_users_list.append(room_users_obj_list[i]['user_id'])

                        counter = self.room_size
                        temp_turn = int(loaded_data.get('turn'))
                        while(counter > 0):
                            temp_turn = (temp_turn+1)%(self.room_size)
                            if temp_turn in room_users_list:
                                turn = temp_turn
                                await self.set_turn(self.room_code, turn)
                                break
                            counter -= 1
                        
                        await self.set_is_round_over(self.room_code, True)
                        q_count = loaded_data.get('q_count')
                        my_response = {
                            "message" : "roundOverMsg",
                            "room_users_dict" : room_users_dict,
                            "turn" : turn,
                            "round_winner" : loaded_data.get('username'),
                            "round_winner_id" : self.user_id,
                            "q_count" : q_count 
                        }
                        await self.channel_layer.group_send(
                            self.room_code,
                            {
                                "type" : "group_msg",
                                "text" : json.dumps(my_response)
                            }
                        )

            elif message == "timerExpiredMessage":
                is_round_over = await self.get_is_round_over(self.room_code)
                if is_round_over == False:
                    await self.set_is_round_over(self.room_code, True)
                    room_users_dict = await self.get_online_users(self.room_code)
                    room_users_obj_list = room_users_dict['room_users']

                    room_users_list = []
                    for i in range(len(room_users_obj_list)):
                        room_users_list.append(room_users_obj_list[i]['user_id'])

                    counter = self.room_size
                    turn = await self.get_turn(self.room_code)
                    temp_turn = turn
                    while(counter > 0):
                        temp_turn = (temp_turn+1)%(self.room_size)
                        if temp_turn in room_users_list:
                            turn = temp_turn
                            await self.set_turn(self.room_code, turn)
                            break
                        counter -= 1
                    
                    q_count = loaded_data.get('q_count')
                    my_response = {
                        "message" : "timerExpiredMessage",
                        "room_users_dict" : room_users_dict,
                        "turn" : turn,
                        "q_count" : q_count
                    }
                    await self.channel_layer.group_send(
                        self.room_code,
                        {
                            "type" : "group_msg",
                            "text" : json.dumps(my_response)
                        }
                    )
            elif message == "gameOverMsg":
                room_users_dict = await self.get_online_users(self.room_code)
                await self.set_game_over(self.room_code)
                my_response = {
                    "message" : "gameOverMsg",
                    "room_users_dict" : room_users_dict,
                }
                await self.channel_layer.group_send(
                    self.room_code,
                    {
                        "type" : "group_msg",
                        "text" : json.dumps(my_response)
                    }
                )

    async def websocket_disconnect(self, event):
        await self.set_offline(self.room_code, self.username)

        room_users_dict = await self.get_online_users(self.room_code)
        turn = await self.get_turn(self.room_code)

        if len(room_users_dict['room_users']) == 0:
            await self.set_game_over(self.room_code)
            await self.set_turn(self.room_code, -1)
        else:
            room_users_obj_list = room_users_dict['room_users']
            room_users_list = []
            for i in range(len(room_users_obj_list)):
                room_users_list.append(room_users_obj_list[i]['user_id'])

            if turn > -1 and turn == self.user_id:
                counter = self.room_size
                temp_turn = turn
                while(counter > 0):
                    temp_turn = (temp_turn+1)%(self.room_size)
                    if temp_turn in room_users_list:
                        turn = temp_turn
                        await self.set_turn(self.room_code, turn)
                        break
                    counter -= 1

            my_response = {
                "message" : "onlineUsersList",
                "room_users_dict" : room_users_dict,
                "turn" : turn
            }

            await self.channel_layer.group_send(
                self.room_code,
                {
                    "type" : "group_msg",
                    "text" : json.dumps(my_response)
                }
            )
        print("disconnected", event)

    @database_sync_to_async
    def get_room_size(self, room_code):
        room = Room.objects.filter(room_code=room_code)[0]
        return room.room_size

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.filter(username=username)[0]

    @database_sync_to_async
    def get_user_id(self, room_code, username):
        user_id = RoomLobby.objects.filter(room_code=room_code, room_user=username)[0].user_id
        return user_id

    @database_sync_to_async
    def get_turn(self, room_code):
        turn = Room.objects.filter(room_code=room_code)[0].turn
        return turn

    @database_sync_to_async    
    def set_turn(self, room_code, turn):
        room = Room.objects.filter(room_code=room_code)[0]
        room.turn = turn
        room.save()

    @database_sync_to_async
    def set_online(self, room_code, username):
        u = RoomLobby.objects.filter(room_code=room_code, room_user=username)[0]
        u.is_online = True
        u.save()

    @database_sync_to_async
    def set_offline(self, room_code, username):
        u = RoomLobby.objects.filter(room_code=room_code, room_user=username)[0]
        u.is_online = False
        u.save()

    @database_sync_to_async
    def get_correct_answer(self, question_no):
        q = Question.objects.filter(question_no=question_no)[0]
        correct_ans = q.answer
        correct_ans = correct_ans.upper()
        return correct_ans

    @database_sync_to_async
    def update_score(self, room_code, username, q_points):
        rl = RoomLobby.objects.filter(room_code=room_code, room_user=username)[0]
        rl.score += q_points
        rl.save()

    @database_sync_to_async
    def get_online_users(self, room_code):
        room_users = RoomLobby.objects.filter(room_code=room_code, is_online=True)
        print(room_users)
        room_users_dict = {
            'room_code' : room_code,
            'room_users' : []
        }
        for ru in room_users:
            item = {
                'room_user' : ru.room_user,
                'score' : ru.score,
                'status' : ru.is_online,
                'user_id': ru.user_id
            }
            room_users_dict['room_users'].append(item)
            print(ru.room_user, ru.is_online)
        return room_users_dict

    @database_sync_to_async
    def get_timer_expired_count(self, room_code):
        room = Room.objects.filter(room_code=room_code)[0]
        return room.timer_expired_count

    @database_sync_to_async
    def set_timer_expired_count(self, room_code, count):
        room = Room.objects.filter(room_code=room_code)[0]
        room.timer_expired_count = count
        room.save()

    @database_sync_to_async
    def set_game_started(self, room_code):
        room = Room.objects.filter(room_code=room_code)[0]
        room.game_started = True
        room.save()

    @database_sync_to_async
    def set_game_over(self, room_code):
        room = Room.objects.filter(room_code=room_code)[0]
        room.game_started = False
        room.save()

    @database_sync_to_async
    def get_questions(self):
        questions = {
            'general_news' : [],
            'entertainment' : [],
            'sports' : [],
            'technology' : []
        }

        q = Question.objects.all()
        temp_general = []
        temp_entertainment = []
        temp_sports = []
        temp_technology = []
        for i in range(len(q)):
            q_dict = {
                    'question_no' : q[i].question_no,
                    'question' : q[i].question,
                    'category' : q[i].category,
                    'points' : q[i].points
                }
            if q[i].category == 'general':
                if q[i].points not in temp_general:
                    temp_general.append(q[i].points) 
                    questions['general_news'].append(q_dict)
            elif q[i].category == 'Entertainment':
                if q[i].points not in temp_entertainment:
                    temp_entertainment.append(q[i].points)
                    questions['entertainment'].append(q_dict)
            elif q[i].category == 'sports':
                if q[i].points not in temp_sports:
                    temp_sports.append(q[i].points)
                    questions['sports'].append(q_dict)
            elif q[i].category == 'Technology':
                if q[i].points not in temp_technology:
                    temp_technology.append(q[i].points)
                    questions['technology'].append(q_dict)

        for k in questions.keys():
            questions[k] = sorted(questions[k], key = lambda i: i['points'])
        return questions
            
    @database_sync_to_async
    def get_is_round_over(self, room_code):
        room = Room.objects.filter(room_code=room_code)[0]
        return room.is_round_over

    @database_sync_to_async
    def set_is_round_over(self, room_code, flag):
        room = Room.objects.filter(room_code=room_code)[0]
        room.is_round_over = flag
        room.save()
