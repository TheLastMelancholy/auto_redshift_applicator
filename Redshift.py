import os
import datetime as dt


class color_frame():
	def __init__(self, t1, t2, T1, T2):
		self.t1 = t1
		self.t2 = t2
		self.T1 = T1
		self.T2 = T2
		#I don't like this solution. But it's 2am
		#Should be at job to aprx. 9-10 am.
		self.cross_day = False
		self.normalize()

	def normalize(self):
		if self.t2<self.t1:
			self.t2 += 24
			self.cross_day = True

	#NOW WORKING WITH HOURS.
	#FIX TO PROCESS MINUITES FOR SMOOTH COLOR TRANSITION 
	def interpolate(self, time):
		#should be separate method. kind of.
		if self.cross_day and time<self.t1:
			time += 24		
		#too many "selfs"
		t_pos = (time - self.t1)/(self.t2 - self.t1)
		#print(t_pos)
		#change namings
		dT = self.T2-self.T1
		return int(self.T1 + dT * t_pos)

	def get_temperature(self, time):
		t_acutal = self.interpolate(time)
		return t_acutal

	def __contains__(self, time):
		#there are should be something better
		#tahn so ~ so flag logic
		if self.cross_day and time<self.t1:
			time = time+24
		return time >= self.t1 and time < self.t2

	def __hash__(self):
		#guess based on literary nothing
		return (self.T2*self.T2)%(self.t1*self.t2)




class color_scheme():
	def __init__(self):
		#idk why
		self.scheme = set()

	def add_frame(self, t1, t2, T1, T2):
		self.scheme.add(color_frame(t1,t2,T1,T2))

	def get_active_color(self, time):
		for frame in self.scheme:
			if time in frame:
				return frame.get_temperature(time)
		#Color frame is not defined. Do not change.
		return None

	def set_color(self, custom_t = None):
		#just for testing
		current_time = dt.datetime.now().hour + dt.datetime.now().minute/60 if custom_t is None else custom_t
		actual_color = self.get_active_color(current_time)
		if actual_color is None:
			print("???")
			return
		else:
			#print(f"redshift -O {actual_color}")
			os.system("redshift -x")
			os.system(f"redshift -O {actual_color}")


#Define timeframes
#Terrible hardcode
#TODO - create config and GUI

#also bad namings ~ scheme/frame - repeating
scheme = color_scheme()
scheme.add_frame(7, 10,3000,4000)
scheme.add_frame(10,11,4000,5000)
scheme.add_frame(11,16,5000,4500)
scheme.add_frame(16,18,4500,4000)
scheme.add_frame(18,21,4000,3500)
scheme.add_frame(21,22,3500,3000)
scheme.add_frame(22,23,3000,2000)
scheme.add_frame(23,4, 2000,1000)
scheme.add_frame(4, 5, 1000,1500)
scheme.add_frame(5, 6, 1500,2000)
scheme.add_frame(6, 7, 2000,3000)

# for i in range(3600):
# 	t = i/60
# 	t = int(t)%24 + (t-int(t))
# 	print(t)
# 	scheme.set_color(t)

scheme.set_color()