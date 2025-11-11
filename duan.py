import json
import pyttsx3
import csv

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class Event:
   def __init__(self,event_name, event_date,event_capacity):
        self.name = event_name
        self.date = event_date
        self.capacity = int(event_capacity)
        self.attendees = []

   def register_attendee(self, attendee_name):
        if attendee_name in self.attendees:
           speak(f'{attendee_name} is already in Event!')
        elif len(self.attendees) >= self.capacity:
           speak(f'Sorry {attendee_name}, {self.name} is full!')
        else:
           self.attendees.append(attendee_name)
           speak(f'Congratulate {attendee_name}! Soon too see you.')
   def attendance_count(self):
      return len(self.attendees)
   
class Event_system:
    def __init__(self):
       self.events=[]                                    
       self.load_data()                                 
    def load_data(self):                                   
       try:
        with open('events.json','r',encoding= 'utf_8') as fhand:           
          data = json.load(fhand)                        
          for e in data:
             event = Event(e['name'],e['date'],e['capacity'])  
             event.attendees = e['attendees']                  
             self.events.append(event)                      
       except FileNotFoundError:
          speak('Please contact admin for support. Sorry about this!')
    def save_event(self):
       data = []
       for e in self.events:                             
          data.append({
             'name':e.name,                               
             'date':e.date,
             'capacity':e.capacity,
             'attendees':e.attendees})
       with open('events.json','w',encoding= 'utf-8') as fhand:
           json.dump(data,fhand,indent = 4,ensure_ascii= False)     


    def add_event(self,name,date,capacity):                       
       for e in self.events:
          if e.name == name and e.date ==date:                                        
           speak('Event already exist!')
           return
       event = Event(name,date,capacity)                             
       self.events.append(event)                                     
       self.save_event()                                             
       speak(f"Event '{name}' added successfully.")

   
    def update_event(self, old_name, new_name, new_date, new_capacity):    
      for e in self.events:                                              
          if e.name == old_name:                                          
             e.name = new_name
             e.date = new_date
             e.capacity = new_capacity
             self.save_event()                                             
             print(f"Event '{old_name}' updated.")
             return
      speak('Event not found!')                                             

   
    def delete_event(self,name):                                                                                
       for e in self.events:                                         
          if e.name == name:                                         
             self.events.remove(e)                                 
             self.save_event()  
             print(f"Event '{name}' deleted.")
             return
       speak('Event not found!')  


    def list_events(self):                                           
       if not self.events:                                           
          speak('No events found!')
          return
       print("\n==================== Event List ====================")                             
       for e in self.events:                                         
          print(f"Event {e.name} - | date: {e.date} | capacity: {len(e.attendees)}/{e.capacity}")      
          print('===================================================')
       print('=======================End=========================')

    def register_for_event(self, event_name,attendee_name):
       for e in self.events:
          if event_name == e.name:
             e.register_attendee(attendee_name)
             self.save_event()
    
    def view_event(self,event_name):                                                                                                
        for e in self.events:
           if event_name == e.name:
              print(f"Event name: {e.name} | date: {e.date} | capacity: {e.attendance_count()}/{e.capacity}")
              found= True
              return
        speak('Event not found!')
           

    def event_attendees(self, event_name ):                     
       for e in self.events:
           if event_name.strip().lower() == e.name.strip().lower():         
              if len(e.attendees) == 0:
                 speak('The event currently has no attendees')
                 return
              else: 
               print(f'Event attendees: {e.attendees}')
               return
       speak('Event not found!')
       
    
    def statistic_events(self):                                    
       if not self.events:                                         
          speak('No events available!')
          return                                                  
       attendees = sum(e.attendance_count() for e in self.events)               
       most_attendees = max(self.events, key =lambda e: e.attendance_count())   
       least_attendees = min(self.events, key = lambda e: e.attendance_count()) 
       print(f'Total attendees of all events: {attendees}')
       print(f"Most attended event: {most_attendees.name} ({len(most_attendees.attendees)} attendees)")               
       print(f"least attended event: {least_attendees.name} ({len(least_attendees.attendees)} attendees)")         
     
    def export_to_CSV(self, filename = 'events.csv'):           
       if not self.events:                                          
          speak('No events to export!')
          return
       with open(filename, 'w', newline = '', encoding = 'utf-8-sig') as csvfile:                                        
        fieldnames = ['Event name', 'Date', 'Capacity', 'Attendees count', 'Attendees List']                         
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)                                              
        writer.writeheader()                                                                                   
        for e in self.events:                                                                                 
         writer.writerow({                                                                                     
           'Event name': e.name,
           'Date':e.date,
           'Capacity':e.capacity,
           'Attendees count': len(e.attendees),
           'Attendees List': ', '.join(e.attendees) if e.attendees else 'No attendees yet'
            }) 
       speak(f" Event data has been successfully exported to file '{filename}'!")                                                                                  

                     
                                      
def speak(audio):
   engine = pyttsx3.init()                                    
   voice = engine.getProperty('voices')                               
   engine.setProperty('voice', voice[1].id)                                
   print('R.O.B.O.T: ' + audio)                                  
   engine.say(audio)                                              
   engine.runAndWait()                                              
   engine.stop()                                                   



def admin_menu(system, user):
    while True:
        print("\n=== Admin Menu ===")
        print("1. Add Event")
        print("2. Update Event")
        print("3. Delete Event")
        print("4. View All Events")
        print("5. View Statistics")
        print("6. Export Events to File CSV")
        print("0. Logout")
        

        choose = input('Enter your choice: ')
        if choose == '1':
           name = input('Event name: ')
           date = input('Event date: ')
           capacity = int(input('Event Capacity: '))
           system.add_event(name,date,capacity)
        elif choose == '2':
           Old_name = input('Old event name: ')
           new_name = input('New name: ')
           new_date = input('New date: ')
           new_capacity = int(input('New capacity: '))
           system.update_event(Old_name, new_name,new_date,new_capacity)
        elif choose == '3':
           name = input('Event name to delete: ')
           system.delete_event(name)
        elif choose == '4':
           system.list_events()
        elif choose == '5':
           system.statistic_events()
        elif choose == '6':
           filename = input('Enter File CSV name: ')
           if filename == '':
              filename = 'events.csv'
           system.export_to_CSV(filename)
        elif choose == '0':
           speak(f'Good bye {user.name}! Nice to meet you.')
           break
        else:
           print('Invalid Choice!')


def organizer_menu(system,user):
   while True:
        print("\n=== Organizer Menu ===")
        print("1. Add Event")
        print("2. View My Event ")
        print("3. View My Attendees ")
        print("4. View All Events")
        print("0. Log out")
        choose = input('Enter your choice: ')

        
        if choose == '1':
           name = input('Event name: ')
           date = input('Event date: ')
           capacity = input('Event Capacity: ')
           system.add_event(name,date,capacity)
        elif choose == '2':
           event_name = input('Enter Event name: ')
           system.view_event(event_name)
        elif choose == '3':
           name = input('Event name: ')
           system.event_attendees(name)
        elif choose == '4':
           system.list_events()
        elif choose == '0':
           speak(f'Good bye {user.name}! Nice to meet you.')
           break
        else:
           print('Invalid Choice!')


def attendee_menu(system,user):
   while True:
       print("\n=== Student/Visitor Menu ===")
       print("1. Register for event")
       print("2. Search Event ")
       print("3. View All Events")
       print("0. Log out")
       choose = input('Enter your choice: ')
       
       if choose == '1':
         event_name = input('Enter Event Name: ')
         attendee_name= input('Enter your full name: ')
         system.register_for_event(event_name, attendee_name)
       elif choose == '2':
          event_name = input('Enter Event Name: ')
          system.view_event(event_name)
       elif choose == '3':
          system.list_events()
       elif choose == '0':
           speak(f'Good bye {user.name}! Nice to meet you.')
           break
       else:
           print('Invalid Choice!')
       

def main():
    system = Event_system()   
    speak('Welcome to Campus Event Management System!')
    username= input('Enter your name: ')
    print('Select role: 1-Admin | 2-Organizer | 3-Student/Visitor ')
    speak(f'Hello {username}, please choose your role: ')
    role_choose = input()
    if role_choose == '1':
        user = User(username, 'Admin')
        admin_menu(system,user)
    elif role_choose == '2':
        user = User(username, 'Organizer')
        organizer_menu(system,user)
    elif role_choose == '3':
        user = User(username, 'Student/Visitor')
        attendee_menu(system,user)
    else: print("Invalid role!")
if __name__ == '__main__':
 main()