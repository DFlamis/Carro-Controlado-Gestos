import pygame as pyg
import math

def move(key, object, speed, sprite, angle, rotation, center, sprite_copy):
    direction = 'none'
    total_angle = angle

    if key[pyg.K_UP]:
        direction = 'Forward'
        axes = getAxes(speed,angle)
        object = object.move(-axes[0],axes[1])

        center = updateCenter(center,-axes[0],axes[1])
    
    if key[pyg.K_DOWN]:
        direction = 'Back'
        axes = getAxes(speed,angle)
        object = object.move(axes[0],-axes[1])

        center = updateCenter(center,axes[0],-axes[1])

    if key[pyg.K_LEFT]:
        direction = 'rotate left'
        total_angle = angle + rotation
        sprite = pyg.transform.rotate(sprite_copy,total_angle)

        object = sprite.get_rect()
        object.center = center

    if key[pyg.K_RIGHT]:
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


def spriteMovement(sprite, speed, angle, rotation, center, key):
    direction = 'None'

    if key[pyg.K_UP]:
        direction = 'Forward'
        axes = getAxes(speed,angle)
        sprite.update(-axes[0], axes[1], angle, center)
    
        center = updateCenter(center, -axes[0], axes[1])

    if key[pyg.K_DOWN]:
        direction = 'Back'
        axes = getAxes(speed,angle)
        sprite.update(axes[0], -axes[1], angle, center)

        center = updateCenter(center, axes[0], -axes[1])

    if key[pyg.K_LEFT]:
        direction = 'rotate left'
        angle += rotation
        sprite.update(0, 0, angle, center)

    if key[pyg.K_RIGHT]:
        direction = 'rotate right'
        angle -= rotation
        sprite.update(0, 0, angle, center)


    return sprite, direction, angle, center

def rot_center(image, angle, x, y):
    
    rotated_image = pyg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect