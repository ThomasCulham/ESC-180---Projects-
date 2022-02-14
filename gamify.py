'''
Gamify


Author: Thomas Culham. Last modified Oct 2020.

'''

def initialize():                  #Defines initial values for all variables.
    global health, hedons, tired, cooldown, L, inflation, runt  # L is a list that contains stars and runt stands for run time
    health = 0
    hedons = 0
    cooldown = 0
    inflation = False
    L = [[0,0],[0,0],[0,0] ]
    tired = False
    runt=0





def perform_activity(a, t):  #Function that preformes every activity.

    global cooldown, health, hedons, tired, L, inflation, runt

    if(cooldown<=0):   #deciding wether the user is tied
        tired = False
    else:
        tired=True

    if(L[2][1]>0):  #sets inflation to true if 3 or more stars are given within the span of 2 hours
        inflation = True

    if(a!="running"):  #resents runt to 0 if running time is interupted
        runt=0

    if(a=="running"):  #Calculates number of health points for running 3*t where t<=180 and then beynd that +=t. If
                       #tired, headons -= 2*t. if star, 3 hedons per seconds up to 10 minutes
        if((t+runt)<=180):
            health += (t*3)
        elif(runt<=180):
            health += (180-runt)*3
            health += (t+runt)-180
        else:
            health+=t

        if(tired):             #points deducted due to exaustion
            hedons -= 2*t
        elif(t<=10):
            hedons+=2*t
        else:
            hedons += 20
            hedons -= 2*(t-10)
        runt+=t

        if(star_can_be_taken("running")):   #points from stars
            if(t>10):
                hedons += 30
            else:
                hedons += 3*t

        cooldown=120    #sets a timer that counts last time running or books was done

    elif(a=="textbooks"):  #Gives 2 points per minute for carrying books.
        health += 2*t
        if(tired):        #points from exaustion
            hedons -= 2*t
        elif(t<=20):
            hedons+=t
        else:
            hedons += 20
            hedons -= (t-20)

        if(star_can_be_taken("textbooks")):   #points from stars
            if(t>10):
                hedons += 30
            else:
                hedons += 3*t

        cooldown=120    #sets a timer that counts last time running or books was done


    elif(a=="resting"):      #Does nothing to headons or health because rest has no direct effect on those points.cooldown-=t
        cooldown -= t

    else:                        #Prints error message if the input is not recognized
        print("Error: Invallid input.")
        print("Input '" + a + "' not recognized")

    for i in range(len(L)):   #substracts t from all star's "expiery date"
        L[i][1]-=t




def get_cur_hedons(): #returns hedons
    global hedons
    return hedons



def get_cur_health(): #returns health
    global health
    return health


def star_can_be_taken(activity): #returns false if inflation or if there is no star for the activity, else true
    global L, inflation

    if(inflation or L[2][1]>0):
        return False

    for i in range(len(L)):
        if(L[i][0]==activity and L[i][1]==120):
            return True

    return False




def offer_star(activity):   # adds a star to list L at index 0. each star is a list that contains a name and an expiery date
    L.insert(0,[activity,120])



def most_fun_activity_minute():  #returns most fun activity bassed on hedons

    if(L[0][1]==120):       #A star automatically makes something more fun than anything else
        return L[0][0]

    if(tired or cooldown>0):  # beter to gain 0 hedons than lose hedons when tired
        return "resting"

    return "running"    #all else equal, running gives more hedons






##                                                      Main Testing Block:                                                    ##




if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons()) # -20 = 10 * 2 + 20 * (-2)
    print(get_cur_health()) # 90 = 30 * 3
    print(most_fun_activity_minute()) # resting
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute()) # running
    perform_activity("textbooks", 30)
    print(get_cur_health()) # 150 = 90 + 30*2
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons()) # -20 = 10 * 2 + 20 * (-2)
    print(get_cur_health()) # 90 = 30 * 3
    print(most_fun_activity_minute()) #resting
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute()) # running
    perform_activity("textbooks", 30)
    print(get_cur_health()) # 150 = 90 + 30*2
    print(get_cur_hedons()) # -80 = -20 + 30 * (-2)
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health()) # 210 = 150 + 20 * 3
    print(get_cur_hedons()) # -90 = -80 + 10 * (3-2) + 10 * (-2)
    perform_activity("running", 170)
    print(get_cur_health()) # 700 = 210 + 160 * 3 + 10 * 1
    print(get_cur_hedons()) # -430 = -90 + 170 * (-2)
    offer_star("running")
    offer_star("textbook")
    print(star_can_be_taken("running")) #True
    print(star_can_be_taken("textbook")) #True
    offer_star("running")
    print(star_can_be_taken("running")) #False
    perform_activity("jog",30) #print error statement

























