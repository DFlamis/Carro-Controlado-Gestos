import pygame as pyg
import math

def move(key, object, speed, sprite, angle, rotation, center, sprite_copy):
    direction = 'none'
    total_angle = angle

    # if key[pyg.K_UP]:
    if key == 'F':
        direction = 'Forward'
        axes = getAxes(speed,angle)
        object = object.move(-axes[0],axes[1])

        center = updateCenter(center,-axes[0],axes[1])
    
    # if key[pyg.K_DOWN]:
    if key == 'B':
        direction = 'Back'
        axes = getAxes(speed,angle)
        object = object.move(axes[0],-axes[1])

        center = updateCenter(center,axes[0],-axes[1])

    # if key[pyg.K_LEFT]:
    if key == 'L':
        direction = 'rotate left'
        total_angle = angle + rotation
        sprite = pyg.transform.rotate(sprite_copy,total_angle)

        object = sprite.get_rect()
        object.center = center

    # if key[pyg.K_RIGHT]:
    if key == 'R':
        direction = 'rotate right'
        total_angle = angle - rotation
        sprite = pyg.transform.rotate(sprite_copy,total_angle)
        
        object = sprite.get_rect()
        object.center = center

    return object.move(0,0), direction, sprite, total_angle, center


def updateCenter(coor, x, y):
    coor[0] += x
    coor[1] += y
    return coor


def getAxes(speed, angle):
    x = speed * ( math.cos( math.radians(angle) ) )
    y = speed * ( math.sin( math.radians(angle) ) )
    return round(x), round(y)


def spritePlayerMovement(sprite, speed, angle, rotation, center, key, factor, second_key):
    direction = 'None'
    

    if (key[pyg.K_UP] or second_key == 'F') and factor:
        direction = 'Forward'
        axes = getAxes(speed,angle)
        sprite.update(-axes[0], axes[1], angle, center)
    
        center = updateCenter(center, -axes[0], axes[1])

    if (key[pyg.K_DOWN] or second_key == 'B') and factor:
        direction = 'Back'
        axes = getAxes(speed,angle)
        sprite.update(axes[0], -axes[1], angle, center)

        center = updateCenter(center, axes[0], -axes[1])

    if (key[pyg.K_LEFT] or second_key == 'L') and factor:
    # if key == 'L':
        direction = 'rotate left'
        angle += rotation
        sprite.update(0, 0, angle, center)

    if (key[pyg.K_RIGHT] or second_key == 'R') and factor:
    # if key == 'R':
        direction = 'rotate right'
        angle -= rotation
        sprite.update(0, 0, angle, center)

    return sprite, direction, angle, center


def spriteNeuronalMovement(sprite, speed, angle, rotation, center, key, all_sensors):
    direction = 'None'
    distance = 0

    # if key[pyg.K_UP]:
    if key == 'UP':
        direction = 'Forward'
        distance = 3
        axes = getAxes(speed,angle)
        sprite.update(-axes[0], axes[1], angle, center)

        angle_helper = 0
        radious = 0
    
        for sensor in all_sensors:
            separator_x = sensor.sprites()[0].separation_x
            separator_y = sensor.sprites()[0].separation_y

            angle_helper = sensor.sprites()[0].angle

            if separator_x != 0:
                radious = separator_x
            else:
                radious = separator_y

            sensor_axes = move_sensor( angle, center, radious, -angle_helper )
            sensor.update( sensor_axes[0], sensor_axes[1], angle )

        center = updateCenter(center, -axes[0], axes[1])

    # if key[pyg.K_DOWN]: #Si, tecnicamente tiene la capacidad de dar patras pero me dio flojera implementar los sensores traseros xd
    if key == 'DOWN':
        direction = 'Back'
        print('Wait this is illegal, saki can not go back')
    #Asi que ahi muere pues si choca no tendra la posibilidad de dar retro y si lo sensores detectan las paredes muy cerca bien puede girar hacia alguna direccion

    # if key[pyg.K_LEFT]: #ARREGLAR
    if key == 'LEFT':
        direction = 'rotate left'
        angle += rotation
        sprite.update(0, 0, angle, center)

        pointer = 0
        radious = 0

        for sensor in all_sensors:
            radious_x = sensor.sprites()[0].separation_x
            radious_y = sensor.sprites()[0].separation_y

            angle_helper = sensor.sprites()[0].angle

            if radious_x != 0:
                radious = radious_x
            else:
                radious = radious_y

            sensor_axes = move_sensor( angle, center, radious, -angle_helper )
            sensor.update( sensor_axes[0] , sensor_axes[1], angle )

            pointer += 1

    # if key[pyg.K_RIGHT]:
    if key == 'RIGHT':
        direction = 'rotate right'
        angle -= rotation

        sprite.update(0, 0, angle, center)

        pointer = 0
        for sensor in all_sensors:
            radious = 0

            radious_x = sensor.sprites()[0].separation_x
            radious_y = sensor.sprites()[0].separation_y

            angle_helper = sensor.sprites()[0].angle

            if radious_x != 0:
                radious = radious_x
            else:
                radious = radious_y

            sensor_axes = move_sensor( angle, center, radious, -angle_helper )
            sensor.update( sensor_axes[0] , sensor_axes[1], angle )

            pointer += 1

    return sprite, direction, angle, center, distance

def move_sensor( angle, center, radious, angle_helper ):

    x = center[0] + (math.cos( math.radians(angle + angle_helper) ) * (-radious))
    y = center[1] + ( math.sin( math.radians(-angle - angle_helper) ) * (-radious) )

    return x,y