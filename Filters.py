import cv2
import math
import random

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    rgb = [r, g, b]
    return tuple(rgb)


def black_or_white():
    color = [[0,0,0],[255,255,255]]
    whiteorblack = random.choice(color)
    return whiteorblack


def init():
    global faceCasscade
    global cap
    face=  cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    #eyesCasscade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    vid = cv2.VideoCapture(0)
    faceCasscade = face
    cap = vid


def detect_face(image):
    face = image.copy()
    detections = faceCasscade.detectMultiScale(face)

    if(len(detections) == 0):
        add_filters()

    else:

        if (len(detections) > 1 ) :
            print(detections.shape)
            #add_filters()

        else:
            if detections[0][2]  > 0 and  detections[0][3] > 0 :

                x =detections[0][0]
                y =detections[0][1]
                h =detections[0][2]
                w =detections[0][3]

                centerpoint_x = math.floor (x+w/2)
                centerpoint_y= math.floor((y+h)/2)

                elipse_width = math.floor(w*0.5)
                elipse_height = math.floor(h*0.5)

                whiteorblack = black_or_white()
                randColor = random_color()

                cv2.ellipse(face, (centerpoint_x, centerpoint_y), (elipse_width, elipse_height), 180, 0, 180,
                            whiteorblack, -1)

                cv2.circle(face, (centerpoint_x - math.floor(w*0.2), centerpoint_y - math.floor(h*0.2) ),
                           10, randColor, 10)

                cv2.circle(face, (centerpoint_x + math.floor(w*0.2), centerpoint_y - math.floor(h*0.2) ),
                           10, randColor, 10)

                line_thickness = 2
                cv2.line(face, ((centerpoint_x - math.floor(w*0.2), centerpoint_y + math.floor(h*0.002) )),
                         (centerpoint_x + math.floor(w*0.2), centerpoint_y + math.floor(h*0.002)),
                         (255, 255, 255), thickness=line_thickness)
                #x_ellipse = math.floor((centerpoint_x - math.floor(detections[0][3]*0.2) + (centerpoint_x + math.floor(detections[0][3]*0.2)))/2)
                #y_ellipse = centerpoint_y + math.floor(detections[0][2]*0.002)
                #cv2.ellipse(face, (x_ellipse, y_ellipse), (math.floor(elipse_width*0.4) , math.floor(elipse_height*0.2)), 0, 0, 180, (255,255,255), -1)
            else :
                return

    return face


def add_filters():

    while (True):

        ret , frame = cap.read(0)
        if ret == True :

            #frame = detect_face(frame )
            frame = detect_face(frame)
            cv2.imshow('Filter',frame )
            k = cv2.waitKey(1)

            if k & 0xFF == ord('q'):
                break
        else :
            print('False')

    cap.release()
    cv2.destroyAllWindows()

init()
add_filters()