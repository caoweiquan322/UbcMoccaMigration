#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Topcoder Inc. All Rights Reserved.

@author: TCSCODER
"""


class Joint(object):
    def __init__(self, json_dict):
        assert json_dict is not None, 'json_dict of Joint constructor must not be None'
        self.ID = -1
        self.Name = None
        self.Type = 'none'
        self.Parent = -1
        self.AttachX = 0
        self.AttachY = 0
        self.AttachZ = 0
        self.AttachThetaX = 0
        self.AttachThetaY = 0
        self.AttachThetaZ = 0
        self.LimLow0 = 1
        self.LimLow1 = 1
        self.LimLow2 = 1
        self.LimHigh0 = 0
        self.LimHigh1 = 0
        self.LimHigh2 = 0
        self.TorqueLim = 0
        self.ForceLim = 0
        self.IsEndEffector = 0
        self.DiffWeight = 1
        self.Offset = 0
        self.parent_joint = None
        self.sub_joints = set()
        self.body_obj = None
        self.draw_shape_obj = None
        self.__dict__.update(json_dict)

    def __eq__(self, other):
        return isinstance(other, Joint) and (
            self.ID == other.ID and self.ID >= 0 or self.Name == other.Name and self.Name is not None)

    def __hash__(self):
        return self.ID if self.ID >= 0 else self.Name

    def is_root(self):
        return self.parent_joint is None

    def add_child(self, joint):
        assert isinstance(joint, Joint), 'the joint object must be a Joint'
        assert joint.Parent == self.ID, 'the joint.Parent to set as child does not match my ID'
        if joint not in self.sub_joints:
            self.sub_joints.add(joint)
        joint.parent_joint = self

    def assign_body(self, body):
        assert isinstance(body, Body)
        body.assign_joint(self)

    def assign_draw_shape(self, draw_shape):
        assert isinstance(draw_shape, DrawShape)
        draw_shape.assign_joint(self)


class Body(object):
    def __init__(self, json_dict):
        assert json_dict is not None, 'json_dict of Body constructor must not be None'
        self.ID = -1
        self.Name = None
        self.Shape = 'box'
        self.Mass = 0
        self.ColGroup = -1
        self.EnableFallContact = 0
        self.AttachX = 0
        self.AttachY = 0
        self.AttachZ = 0
        self.AttachThetaX = 0
        self.AttachThetaY = 0
        self.AttachThetaZ = 0
        self.Param0 = 0
        self.Param1 = 0
        self.Param2 = 0
        self.ColorR = 0.8
        self.ColorG = 0.3
        self.ColorB = 0.2
        self.ColorA = 1.0
        self.joint_obj = None
        self.__dict__.update(json_dict)

    def __eq__(self, other):
        return isinstance(other, Body) and self.ID == other.ID and self.Name == other.Name

    def __hash__(self):
        return self.ID

    def assign_joint(self, joint: Joint):
        assert self.ID == joint.ID or self.ID < 0 and self.Name == joint.Name,\
            'the joint.ID to assign does not match the body.ID'
        self.joint_obj = joint
        joint.body_obj = self


class DrawShape(object):
    def __init__(self, json_dict):
        assert json_dict is not None, 'json_dict of DrawShape constructor must not be None'
        self.ID = -1
        self.Name = None
        self.Shape = 'box'
        self.ParentJoint = -1
        self.AttachX = 0
        self.AttachY = 0
        self.AttachZ = 0
        self.AttachThetaX = 0
        self.AttachThetaY = 0
        self.AttachThetaZ = 0
        self.Param0 = 0
        self.Param1 = 0
        self.Param2 = 0
        self.ColorR = 0.8
        self.ColorG = 0.3
        self.ColorB = 0.2
        self.ColorA = 1.0
        self.joint_obj = None
        self.__dict__.update(json_dict)

    def assign_joint(self, joint: Joint):
        assert self.ParentJoint == joint.ID or self.ID < 0 and self.Name == joint.Name,\
            'the joint.ID to assign does not match the drawShape.ID (%s != %s)' % (str(joint.ID), str(self.ParentJoint))
        self.joint_obj = joint
        joint.draw_shape_obj = self
