import pyglet
import resources
import math
from pyglet.window import *

#Variables
#===========================================
game_screen = 0
key_left_press = False
key_right_press = False
key_up_press = False
key_down_press = False
key_gun_press = False
key_melee_press = False
key_dash_press = False

Player_Bullets = []
Enemy_Bullets = []
Player_melee = []
Enemy_list = []

#Set up window
game_window = pyglet.window.Window(600,800)

#Setting Image layers
group_background = pyglet.graphics.OrderedGroup(0)
group_midground = pyglet.graphics.OrderedGroup(1)
group_foreground = pyglet.graphics.OrderedGroup(2)

#Start/Continue button
spr_btn_start = pyglet.sprite.Sprite(img=resources.button_start, x=300, y=200,group=group_foreground)
spr_btn_continue = pyglet.sprite.Sprite(img=resources.button_continue, x=120, y=640,group=group_foreground)
spr_btn_ng= pyglet.sprite.Sprite(img=resources.button_ng, x=120, y=550,group=group_foreground)
spr_btn_score = pyglet.sprite.Sprite(img=resources.button_score, x=120, y=460,group=group_foreground)
spr_btn_help = pyglet.sprite.Sprite(img=resources.button_help, x=120, y=370,group=group_foreground)

#set up background
game_background = pyglet.sprite.Sprite(img=resources.cover_image,x=300,y=400,group=group_background)
game_background_2 = pyglet.sprite.Sprite(img=resources.bg_image,x=300,y=400,group=group_background)

#menu background
game_menu = pyglet.sprite.Sprite(img=resources.menu_image,x=300,y=400,group=group_background)

#game sprites
spr_player = pyglet.sprite.Sprite(img=resources.player_image,x=300,y=50,group=group_foreground)
spr_player_bullets = []
spr_enemy_list = []
spr_enemy_bullets = []
	
#Set cursor
cursor = pyglet.window.ImageMouseCursor(resources.cursor_1, 16, 8)
#game_window.set_mouse_cursor(cursor)

#dot sprite
dot = pyglet.sprite.Sprite(img=resources.dot_blue, x=40, y=40, group=group_foreground)

#Delete this someday
temp_x = 0
temp_y = 0

pause = False

@game_window.event
def on_draw():
	global game_screen, spr_player_bullets, Player_Bullets, Enemy_list, Enemy_Bullets, spr_enemy_bullets, spr_btn_continue, spr_btn_ng, spr_btn_score, spr_btn_help
	if game_screen == 0:
		game_window.clear()
		game_background.draw()
		spr_btn_start.draw()
	elif game_screen == 1:
		game_window.clear()
		game_menu.draw()
		spr_btn_continue.draw()
		spr_btn_ng.draw()
		spr_btn_score.draw()
		spr_btn_help.draw()
	elif game_screen == 2:
		if pause == False:
			game_window.clear()
			game_background_2.draw()
			spr_player.rotation = rotate_sprite(temp_x,temp_y)
			spr_player.scale = 0.5
			spr_player.draw()

			#===================================Drawing Player bullets=======================
			spr_player_bullets = []
			for b in Player_Bullets:
				if b.modifiers["homing"] and b.modifiers["explosive"]:
					spr_player_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_exhoming,x=b.obj_x,y=b.obj_y,group=group_midground))
				elif b.modifiers["homing"]:
					spr_player_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_homing,x=b.obj_x,y=b.obj_y,group=group_midground))
				elif b.modifiers["explosive"]:
					spr_player_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_explosive,x=b.obj_x,y=b.obj_y,group=group_midground))
				elif b.modifiers["piercing"]:
					spr_player_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_piercing,x=b.obj_x,y=b.obj_y,group=group_midground))
				else:
					spr_player_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_player,x=b.obj_x,y=b.obj_y,group=group_midground))
			for b in spr_player_bullets:
				b.draw()

			#===================================Drawing Enemy bullet==============================
			spr_enemy_bullets = []
			for b in Enemy_Bullets:
				if b.modifiers["homing"] and b.modifiers["explosive"]:
					spr_enemy_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_exhoming,x=b.obj_x,y=b.obj_y,group=group_midground))
				elif b.modifiers["homing"]:
					spr_enemy_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_homing,x=b.obj_x,y=b.obj_y,group=group_midground))
				elif b.modifiers["explosive"]:
					spr_enemy_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_explosive,x=b.obj_x,y=b.obj_y,group=group_midground))
				elif b.modifiers["piercing"]:
					spr_enemy_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_piercing,x=b.obj_x,y=b.obj_y,group=group_midground))
				else:
					spr_enemy_bullets.append(pyglet.sprite.Sprite(img=resources.bullet_enemy,x=b.obj_x,y=b.obj_y,group=group_midground))
				spr_enemy_bullets[-1].rotation=(rotate_sprite(b.obj_vx, b.obj_vy)+180)/2
			for b in spr_enemy_bullets:
				b.draw()

			spr_enemy_list = []
			for b in Enemy_list:
				if b.id == "easy_1":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_1_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "easy_2":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_2_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "easy_3":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_3_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "easy_4":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_4_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "med_1":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_5_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "med_2":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_6_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "med_3":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_7_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "hard_1":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_8_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "hard_2":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_9_image,x=b.x,y=b.y,group=group_foreground))
				if b.id == "hard_3":
					spr_enemy_list.append(pyglet.sprite.Sprite(img=resources.enemy_10_image,x=b.x,y=b.y,group=group_foreground))
			for b in spr_enemy_list:
				b=shrink_2(b)
				b.draw()
@game_window.event
def on_mouse_press(x,y,button,modifiers):
	#==================================
	#Checking if mouse is over buttons
	#==================================
	global game_screen
	if game_screen == 0:
		if abs(x-spr_btn_start.x)<50 and abs(y-spr_btn_start.y)<40:
			game_screen = 1
	elif game_screen == 1:
		if abs(x-spr_btn_ng.x)<50 and abs(y-spr_btn_ng.y)<40:
			game_screen = 2

@game_window.event
def on_mouse_motion(x,y,dx,dy):
	global game_screen, spr_btn_start, spr_btn_ng, spr_btn_continue, spr_btn_score, spr_btn_help
	if game_screen == 0:
		if abs(x-spr_btn_start.x)<50 and abs(y-spr_btn_start.y)<40:
			spr_btn_start = enlarge(spr_btn_start)
		else:
			spr_btn_start = shrink(spr_btn_start)
	if game_screen == 1:
		if abs(x-spr_btn_ng.x)<50 and abs(y-spr_btn_ng.y)<40:
			spr_btn_ng = enlarge(spr_btn_ng)
		else:
			spr_btn_ng = shrink(spr_btn_ng)
		if abs(x-spr_btn_continue.x)<50 and abs(y-spr_btn_continue.y)<40:
			spr_btn_continue = enlarge(spr_btn_continue)
		else:
			spr_btn_continue = shrink(spr_btn_continue)
		if abs(x-spr_btn_score.x)<50 and abs(y-spr_btn_score.y)<40:
			spr_btn_score = enlarge(spr_btn_score)
		else:
			spr_btn_score = shrink(spr_btn_score)
		if abs(x-spr_btn_help.x)<50 and abs(y-spr_btn_help.y)<40:
			spr_btn_help = enlarge(spr_btn_help)
		else:
			spr_btn_help = shrink(spr_btn_help)

@game_window.event
def on_key_press(symbol, modifiers):
	global key_left_press,key_right_press,key_up_press,key_down_press,key_gun_press,key_melee_press,key_dash_press
	global temp_y, temp_x
	if symbol == key.W:
		key_up_press = True
		temp_y = 1
	if symbol == key.A:
		key_left_press = True
		temp_x = -1
	if symbol == key.S:
		key_down_press = True
		temp_y = -1
	if symbol == key.D:
		key_right_press = True
		temp_x = 1
	if symbol == key.R:
		key_gun_press = True
	if symbol == key.T:
		key_melee_press = True
	if symbol == key.Y:
		key_dash_press = True

@game_window.event
def on_key_release(symbol, modifiers):
	global key_left_press,key_right_press,key_up_press,key_down_press,key_gun_press,key_melee_press,key_dash_press
	global temp_x,temp_y
	if symbol == key.W:
		key_up_press = False
		temp_y =0
	if symbol == key.A:
		key_left_press = False
		temp_x = 0
	if symbol == key.S:
		key_down_press = False
		temp_y = 0
	if symbol == key.D:
		key_right_press = False
		temp_x =0
	if symbol == key.R:
		key_gun_press = False
	if symbol == key.T:
		key_melee_press = False
	if symbol == key.Y:
		key_dash_press = False


def on_run():
	pyglet.app.run()

def recieve_vars(game_screen_val):
	global game_screen
	game_screen = game_screen_val

def player_move(x,y):
	global spr_player
	spr_player.x = x
	spr_player.y = y

def update_bullet_list(p_bullet,e_bullet):
	global Player_Bullets, Enemy_Bullets
	Player_Bullets = p_bullet
	Enemy_Bullets = e_bullet

def update_enemy_list(e_list):
	global Enemy_list
	Enemy_list = e_list

def keyboard(key): #When main checks if a certain key is being checked
	global key_left_press,key_right_press,key_up_press,key_down_press,key_gun_press,key_melee_press,key_dash_press
	if key == "up":
		return key_up_press
	if key == "down":
		return key_down_press
	if key == "left":
		return key_left_press
	if key == "right":
		return key_right_press
	if key == "gun":
		return key_gun_press
	if key == "melee":
		return key_melee_press
	if key == "dash":
		return key_dash_press

def get_player_coordinates():
	global spr_player
	return [spr_player.x, spr_player.y]

def change_dot(status):
	if status:
		dot.image = resources.dot_blue
	else:
		dot.image = resources.dot_red

def game_start():
	global game_screen
	if game_screen == 2:
		return True
	else:
		return False

def rotate_sprite(vx, vy):
	if vx != 0:
		degree = math.degrees(math.atan(vy/vx))
		if vy < 0:
			degree+=180
		if vy == 0 and vx > 0:
			degree = 90
		if vy == 0 and vx < 0:
			degree = 270
	elif vy>=0:
		degree = 0
	else:
		degree = 180
	return degree

def enlarge(spr):
	spr.scale = 1.1
	return spr

def shrink(spr):
	spr.scale = 1
	return spr

def shrink_2(spr):
	spr.scale = 0.5
	return spr

def paused(stat):
	global pause
	pause = stat