#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Topcoder Inc. All Rights Reserved.

@author: TCSCODER
"""
from enum import Enum


class Mjcf(object):
    """
    MJCF format I/O object.
    """
    pass

# Below are elements.


class EleTag(Enum):
    # Core tags.
    light = 0
    body = 1
    geom = 2
    joint = 3
    site = 4
    mesh = 5
    skin = 6
    height_field=7
    texture = 8
    material = 9
    camera = 10
    # External tags.
    reference_pose = 50
    spring_reference_pose = 51
    tendon = 52
    actuator = 53
    sensor = 54
    equality = 55
    contact_pair = 56
    contact_exclude = 57
    custom_numeric = 58
    custom_text = 59
    custom_tuple = 60
    keyframe = 61
    # Those unknown ones.
    unknown = 100


class Element(object):
    def __init__(self, tag=EleTag.unknown, name=None):
        self.tag = tag
        self.name = name

# Below is light.


class Light(Element):
    def __init__(self, pos=None, dir=None, diffuse=None, name=None):
        super(Light, self).__init__(tag=EleTag.light, name=name)
        self.pos = pos
        self.dir = dir
        self.diffuse = diffuse

# Below is camera.


class Camera(Element):
    def __init__(self, pos=None, dir=None, name=None):
        super(Camera, self).__init__(tag=EleTag.camera, name=name)
        self.pos = pos
        self.dir = dir

# Below is body.


class Body(Element):
    def __init__(self, mass=None, inertia=None, name=None):
        super(Body, self).__init__(tag=EleTag.body, name=name)
        self.mass = mass
        self.inertia = inertia
        self.geoms = []
        self.sub_bodies = []
        self.sites = []
        self.joints_to_parent = []
        self.parent = None

    def add_geom(self, geom: Geom):
        self.geoms.append(geom)

    def add_body(self, body):
        self.sub_bodies.append(body)
        body.set_parent(self)

    def set_parent(self, parent):
        self.parent = parent

    def add_site(self, site: Site):
        self.sites.append(site)

    def add_joint_to_parent(self, joint: Joint):
        self.joints_to_parent.append(joint)

# Below are geometries.


class GeomType(Enum):
    box = 0
    sphere = 1
    capsule = 2
    cylinder = 3
    ellipsoid = 4


class Geom(Element):
    def __init__(self, geom_type=None, density=1000, name=None):
        super(Geom, self).__init__(tag=EleTag.geom, name=name)
        self.geom_type = geom_type
        self.density = density


class Box(Geom):
    def __init__(self, pos=None, size=None, name=None):
        super(Box, self).__init__(geom_type=GeomType.box, name=name)
        self.pos = pos
        self.size = size


class Sphere(Geom):
    def __init__(self, pos=None, size=None, name=None):
        super(Sphere, self).__init__(geom_type=GeomType.sphere, name=name)
        self.pos = pos
        self.size = size


class Capsule(Geom):
    def __init__(self, from_to=None, size=None, name=None):
        super(Capsule, self).__init__(geom_type=GeomType.capsule, name=name)
        self.from_to = from_to
        self.size = size


class Cylinder(Geom):
    def __init__(self, from_=None, to=None, size=None, name=None):
        super(Cylinder, self).__init__(geom_type=GeomType.cylinder, name=name)
        self.from_ = from_
        self.to = to
        self.size = size


class Ellipsoid(Geom):
    def __init__(self, pos=None, size=None, name=None):
        super(Ellipsoid, self).__init__(geom_type=GeomType.ellipsoid, name=name)
        self.pos = pos
        self.size = size

# Below are joints.


class JointType(Enum):
    hinge = 0
    slide = 1
    fixed = 2
    ball = 3
    free = 4


class Joint(Element):
    def __init__(self, joint_type=None, name=None):
        super(Joint, self).__init__(tag=EleTag.joint, name=name)
        self.joint_type = joint_type


class HingeJoint(Joint):
    def __init__(self, pos=None, axis=None, name=None):
        super(HingeJoint, self).__init__(joint_type=JointType.hinge, name=name)
        self.pos = pos
        self.axis = axis


class SlideJoint(Joint):
    def __init__(self, pos=None, axis=None, name=None):
        super(SlideJoint, self).__init__(joint_type=JointType.slide, name=name)
        self.pos = pos
        self.axis = axis


class FixedJoint(Joint):
    def __init__(self, name=None):
        super(FixedJoint, self).__init__(joint_type=JointType.fixed, name=name)


class BallJoint(Joint):
    def __init__(self, pos=None, name=None):
        super(BallJoint, self).__init__(joint_type=JointType.ball, name=name)
        self.pos = pos


class FreeJoint(Joint):
    def __init__(self, name=None):
        super(FreeJoint, self).__init__(joint_type=JointType.free, name=name)


# Below are sites.


class SiteType(Enum):
    sphere = 0
    box = 1
    capsule = 2
    cylinder = 3
    ellipsoid = 4


class Site(Element):
    def __init__(self, site_type=None, name=None):
        super(Site, self).__init__(tag=EleTag.site, name=name)
        self.site_type = site_type


class SphereSite(Site):
    def __init__(self, pos=None, size=None, name=None):
        super(SphereSite, self).__init__(site_type=SiteType.sphere, name=name)
        self.pos = pos
        self.size = size


class BoxSite(Site):
    def __init__(self, pos=None, size=None, name=None):
        super(BoxSite, self).__init__(site_type=SiteType.box, name=name)
        self.pos = pos
        self.size = size


# Below are assets.


class Mesh(Element):
    def __init__(self, name='__rename_this__'):
        super(Mesh, self).__init__(tag = EleTag.mesh, name=name)


class Skin(Element):
    def __init__(self, name='__rename_this__'):
        super(Skin, self).__init__(tag = EleTag.skin, name=name)
        raise NotImplementedError()


class HeightField(Element):
    def __init__(self, name='__rename_this__'):
        super(HeightField, self).__init__(tag = EleTag.height_field, name=name)


class Texture(Element):
    def __init__(self, name='__rename_this__'):
        super(Texture, self).__init__(tag = EleTag.texture, name=name)


class Material(Element):
    def __init__(self, name='__rename_this__'):
        super(Material, self).__init__(tag = EleTag.material, name=name)


