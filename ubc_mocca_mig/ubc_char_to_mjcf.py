#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Topcoder Inc. All Rights Reserved.

@author: TCSCODER
"""
import json
import numpy as np
from ubc_mocca_mig.ubc_character import Joint as UbcJoint
from ubc_mocca_mig.ubc_character import Body as UbcBody
from ubc_mocca_mig.ubc_character import DrawShape as UbcDrawShape
import xml.dom.minidom as minidom


def add_joints_to_body(ubc_joint: UbcJoint, mjcf_body, xml_doc):
    mjcf_joints_to_add = []
    # Create mjcf joints according to the ubc joint.
    ubc_j_type = ubc_joint.Type
    mjcf_body.setAttribute('pos', '%.5f %.5f %.5f' % (
        ubc_joint.AttachX, ubc_joint.AttachY, ubc_joint.AttachZ))
    mjcf_body.setAttribute('euler', '%.5f %.5f %.5f' % (ubc_joint.AttachThetaX, ubc_joint.AttachThetaY,
                                                        ubc_joint.AttachThetaZ))
    if ubc_joint.is_root() and ubc_j_type == 'none':  # Free
        mjcf_joint = xml_doc.createElement('joint')
        mjcf_joint.setAttribute('type', 'free')
        mjcf_joints_to_add.append(mjcf_joint)
    elif ubc_j_type == 'spherical':  # Ball
        mjcf_joint = xml_doc.createElement('joint')
        mjcf_joint.setAttribute('type', 'ball')
        mjcf_joints_to_add.append(mjcf_joint)
    elif ubc_j_type == 'revolute':  # Hinge
        mjcf_joint = xml_doc.createElement('joint')
        mjcf_joint.setAttribute('type', 'hinge')
        mjcf_joint.setAttribute('axis', '0 0 1')
        mjcf_joints_to_add.append(mjcf_joint)
    elif ubc_j_type == 'prismatic':  # Slide
        mjcf_joint = xml_doc.createElement('joint')
        mjcf_joint.setAttribute('type', 'slide')
        mjcf_joint.setAttribute('axis', '0 0 1')
        mjcf_joints_to_add.append(mjcf_joint)
    elif ubc_j_type == 'planar':  # Slide*2 + Hinge*1
        assert ubc_joint.is_root(), 'planar joint must be root joint'
        # Slide X
        mjcf_joint = xml_doc.createElement('joint')
        mjcf_joint.setAttribute('type', 'slide')
        mjcf_joint.setAttribute('axis', '1 0 0')
        mjcf_joints_to_add.append(mjcf_joint)
        # Slide Y
        mjcf_joint = xml_doc.createElement('joint')
        mjcf_joint.setAttribute('type', 'slide')
        mjcf_joint.setAttribute('axis', '0 1 0')
        mjcf_joints_to_add.append(mjcf_joint)
        # Hinge Z
        mjcf_joint = xml_doc.createElement('joint')
        mjcf_joint.setAttribute('type', 'hinge')
        mjcf_joint.setAttribute('axis', '0 0 1')
        mjcf_joints_to_add.append(mjcf_joint)
    elif ubc_j_type == 'fixed':  #
        pass  # raise RuntimeError('Fixed joint not implemented yet')
    else:
        raise ValueError('Unhandled joint type: %s' % ubc_j_type)
    # Collect the joints we just created.
    for j in mjcf_joints_to_add:
        mjcf_body.appendChild(j)


def add_geom_to_body(ubc_body: UbcBody, mjcf_body, xml_doc):
    mjcf_geom = xml_doc.createElement('geom')
    mjcf_geom.setAttribute('type', ubc_body.Shape)  # Most shape names are compatible.
    mjcf_geom.setAttribute('rgba', '%.2f %.2f %.2f %.2f' % (ubc_body.ColorR, ubc_body.ColorG,
                                                            ubc_body.ColorB, ubc_body.ColorA))
    mjcf_geom.setAttribute('mass', '%.5f' % ubc_body.Mass)
    mjcf_geom.setAttribute('pos', '%.5f %.5f %.5f' % (ubc_body.AttachX, ubc_body.AttachY, ubc_body.AttachZ))
    mjcf_geom.setAttribute('euler',
                           '%.5f %.5f %.5f' % (ubc_body.AttachThetaX, ubc_body.AttachThetaY, ubc_body.AttachThetaZ))
    ubc_shape = ubc_body.Shape
    if ubc_shape == 'sphere':
        mjcf_geom.setAttribute('size', '%.5f' % (ubc_body.Param0/2))
    elif ubc_shape == 'box':
        mjcf_geom.setAttribute('size', '%.5f %.5f %.5f' % (ubc_body.Param0/2, ubc_body.Param1/2, ubc_body.Param2/2))
    elif ubc_shape == 'capsule':
        mjcf_geom.setAttribute('size', '%.5f %.5f' % (ubc_body.Param0/2, ubc_body.Param1/2))
        # UBC capsule is in [0,1,0] direction, while MJCF capsule is in [0,0,1] direction.
        # So we need use rotation matrix: R' = R*rot_x(-pi/2).
        # Since we have R = rot_z(z)*rot_y(y)*rot_x(x) under UBC notation, thus R' = rot_z(z)*rot_y(y)*rot_x(x-pi/2).
        mjcf_geom.setAttribute('euler',
                               '%.5f %.5f %.5f' % (ubc_body.AttachThetaX-np.pi/2,
                                                   ubc_body.AttachThetaY, ubc_body.AttachThetaZ))
    elif ubc_shape == 'cylinder':
        mjcf_geom.setAttribute('size', '%.5f %.5f' % (ubc_body.Param0/2, ubc_body.Param1/2))
        mjcf_geom.setAttribute('euler',
                               '%.5f %.5f %.5f' % (ubc_body.AttachThetaX - np.pi / 2,
                                                   ubc_body.AttachThetaY, ubc_body.AttachThetaZ))
    elif ubc_shape == 'plane':
        mjcf_geom.setAttribute('size', '%.5f %.5f %.5f' % (ubc_body.Param0, ubc_body.Param1, ubc_body.Param2))
    else:
        raise ValueError('Unhandled UBC shape: [%s]' % ubc_shape)
    mjcf_body.appendChild(mjcf_geom)


def dump_kinematic_tree_as_mjcf(root_ubc_joint: UbcJoint, curr_mjcf_body, xml_doc):
    # assert root_joint is not None and root_joint.is_root(), 'root joint is illegal'
    print('Joint: %s' % root_ubc_joint.Name)
    # Body.
    mjcf_body = xml_doc.createElement('body')
    ubc_body = root_ubc_joint.body_obj
    if ubc_body is not None and ubc_body.Name is not None:
        mjcf_body.setAttribute('name', ubc_body.Name)
    curr_mjcf_body.appendChild(mjcf_body)

    # Joints
    add_joints_to_body(root_ubc_joint, mjcf_body, xml_doc)

    # Geoms
    if ubc_body is not None:
        add_geom_to_body(ubc_body, mjcf_body, xml_doc)

    # Process children skeleton.
    for child_mjcf_joint in root_ubc_joint.sub_joints:
        dump_kinematic_tree_as_mjcf(child_mjcf_joint, mjcf_body, xml_doc)


def save_ubc_kinematic_as_mjcf(root_ubc_joint: UbcJoint, file_path: str):
    assert file_path is not None and len(file_path.strip()) > 0, 'file_path could not be empty'
    # The root mujoco
    xml_doc = minidom.getDOMImplementation().createDocument(None, 'mujoco', None)
    mjcf_root = xml_doc.documentElement
    # The option.
    mjcf_option = xml_doc.createElement('option')
    mjcf_option.setAttribute('gravity', '0 -9.81 0')
    mjcf_root.appendChild(mjcf_option)
    # The compiler
    mjcf_compiler = xml_doc.createElement('compiler')
    mjcf_compiler.setAttribute('coordinate', 'local')
    mjcf_compiler.setAttribute('angle', 'radian')  # Default: degree
    mjcf_compiler.setAttribute('eulerseq', 'XYZ')  # Default: xyz
    mjcf_root.appendChild(mjcf_compiler)
    # The world body
    mjcf_world_body = xml_doc.createElement('worldbody')
    mjcf_root.appendChild(mjcf_world_body)
    # The world_body/camera.
    mjcf_camera = xml_doc.createElement('camera')
    mjcf_camera.setAttribute('pos', '0 0.5 5')
    mjcf_camera.setAttribute('fovy', '90')
    mjcf_world_body.appendChild(mjcf_camera)
    # The bodies
    dump_kinematic_tree_as_mjcf(root_ubc_joint, mjcf_world_body, xml_doc)
    # Write file.
    with open(file_path.strip(), 'w', encoding='utf-8') as fxml:
        xml_doc.writexml(fxml, addindent='\t', newl='\n', encoding='utf-8')


def parse_ubc_character_kinematic(file_path: str) -> UbcJoint:
    try:
        assert file_path is not None and len(file_path.strip()) > 0, 'UBC character file path can not be empty'
        with open(file_path) as fin:
            ubc_char = json.load(fin)
            assert ubc_char is not None, 'the character json is empty'
            print(ubc_char)
            accepted_keys = {'Skeleton', 'BodyDefs', 'DrawShapeDefs'}
            skeleton = ubc_char['Skeleton']
            joints = skeleton['Joints']
            bodies = ubc_char['BodyDefs']
            draw_shapes = ubc_char['DrawShapeDefs']

            # Parse joints.
            all_joints = []
            all_id_joints = dict()
            all_named_joints = dict()
            idx = 0
            for joint_dic in joints:
                if 'ID' not in joint_dic:
                    joint_dic['ID'] = idx  # Set array index as the joint ID
                j = UbcJoint(joint_dic)
                assert j.ID not in all_id_joints, 'Found duplicated joint ID [%s]' % j.ID
                if j.ID >= 0:
                    all_id_joints[j.ID] = j
                if j.Name is not None and len(j.Name) > 0:
                    all_named_joints[j.Name] = j
                all_joints.append(j)
                idx += 1
            for j in all_joints:
                if j.Parent in all_id_joints:
                    all_id_joints[j.Parent].add_child(j)
            # Parse bodies.
            idx = 0
            for body_dic in bodies:
                if 'ID' not in body_dic:
                    body_dic['ID'] = idx
                b = UbcBody(body_dic)
                assert b.ID in all_id_joints or b.Name in all_named_joints, 'illegal body found, id=[%s], name=[%s]' % (
                    str(b.ID), b.Name)
                if b.ID in all_id_joints:
                    b.assign_joint(all_id_joints[b.ID])
                elif b.Name in all_named_joints:
                    b.assign_joint(all_named_joints[b.Name])
                idx += 1
            # Parse shapes.
            for draw_shape_dict in draw_shapes:
                ds = UbcDrawShape(draw_shape_dict)
                assert ds.ParentJoint in all_id_joints or ds.Name in all_named_joints, 'illegal draw shape found, id=[%s], name=[%s]' % (
                    str(ds.ID), ds.Name)
                if ds.ParentJoint in all_id_joints:
                    ds.assign_joint(all_id_joints[ds.ParentJoint])
                elif ds.Name in all_named_joints:
                    ds.assign_joint(all_named_joints[ds.Name])

            # Dump ignored parts.
            for k in ubc_char:
                if k not in accepted_keys:
                    print('Ignore unexpected entry [.%s]' % k)

            for k in skeleton:
                if k != 'Joints':
                    print('Ignored key [.Skeleton.%s]' % k)

            # Print kinematic tree.
            trees = []
            for j in all_joints:
                if j.is_root():
                    trees.append(j)
            print('Found %d separate kinematic trees.' % len(trees))
            assert len(trees) == 1, 'The UBC MOCCA character file usually contains one unique body kinematic tree'

            # Return root of the tree
            return trees[0]
    except Exception as e:
        print('Error occurs parsing character file. Details: ', e)
        return None


def main():
    file_path = '../data/UbcMocca/characters/biped3d_full_mocap.txt'
    # file_path = '/Users/fatty/TfDyn/xbpeng/DeepMimic/data/characters/humanoid3d.txt'
    file_path = '../data/UbcMocca/characters/goat.txt'
    root_ubc_joint = parse_ubc_character_kinematic(file_path)
    save_ubc_kinematic_as_mjcf(root_ubc_joint, '../dev/cvt_example.xml')


if __name__ == '__main__':
    main()
