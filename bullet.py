import pyglet
import collision as col

def bullet_action(bullet,target_list,time_elapse):
	bullet.obj_x += bullet.obj_vx
	bullet.obj_y += bullet.obj_vy
	bullet.obj_vx += bullet.obj_ax
	bullet.obj_vy += bullet.obj_ay
	#Update bullet location
	#Just add more behavior like if bullet is homing etc
	if bullet.modifiers["homing"] and len(target_list)>0:
		closest = target_list[0]
		distance = col.get_distance(bullet.obj_x,bullet.obj_y,target_list[0].x,target_list[0].y)
		for t in target_list:
			temp = col.get_distance(bullet.obj_x,bullet.obj_y,t.x,t.y)
			if temp < distance and temp < 400:
				distance = temp
				closest = t
		if abs(closest.x-bullet.obj_x) < 20:
			bullet.obj_vx = 0
		elif closest.x < bullet.obj_x:
			bullet.obj_vx -= 1
		elif closest.x > bullet.obj_x:
			bullet.obj_vx += 1

	if bullet.obj_y > 800:
		bullet.destroy = True
	try:
		for target in target_list:
			if col.get_distance(bullet.obj_x,bullet.obj_y,target.x,target.y) <= 40:
				bullet.destroy = True
				target.life -= 100	#insta kill as of now
	except:
		if col.get_distance(bullet.obj_x,bullet.obj_y,target[0],target[1]) <= 40:
			bullet.destroy = True
			target.life -= 1

	return bullet

def bullet_action_no_collision(bullet):
	bullet.obj_x += bullet.obj_vx
	bullet.obj_y += bullet.obj_vy
	bullet.obj_vx += bullet.obj_ax
	bullet.obj_vy += bullet.obj_ay

	if bullet.obj_y < 0:
		bullet.destroy = True
	return bullet

class bullet(object):
	def __init__(self):
		super(bullet, self).__init__()
		self.obj_x = 0		#Initial position
		self.obj_y = 0		
		self.obj_vx = 0		#Initial velocity
		self.obj_vy = 0
		self.obj_ax = 0		#Acceleration (0 if bullet speed is constant)
		self.obj_ay = 0
		self.modifiers = {"homing":False,"explosive":False,"piercing":False} #piercing,homing, etc
		self.destroy = False

class melee(object):
	def __init__(self):
		super(melee, self).__init__()
		self.arg = arg
		
