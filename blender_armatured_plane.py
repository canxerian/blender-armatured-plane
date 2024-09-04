import bpy
import mathutils

bl_info = {
    "name": "Plane with armature",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Create a plane with 6 bones",
    "author": "Mark Nguyen",
    "version": (1, 0, 0),
    "doc_url": "https://github.com/canxerian/blender-armatured-plane",
    "location": "View3D > Add > Mesh > Plane with Armature"
}


class ArmaturedPlane(bpy.types.Operator):
    """Create plane with armature"""
    bl_idname = "mesh.plane_with_armature"
    bl_label = "Plane with Armature"
    bl_options = {'REGISTER', 'UNDO'}

    size: bpy.props.FloatProperty(name="Size", default=2.0, min=0.1)
    bone_length: bpy.props.FloatProperty(name="Bone length (percentage of size)", default=0.15, min=0.0, max=1.0)
    aspect: bpy.props.FloatProperty(name="Aspect", default=1.78)
    subdivisions: bpy.props.IntProperty(name="Subdivisions", default=10, min=1)
    
    def execute(self, context):
        width = self.size * self.aspect;
        height = self.size;
        
        # Create a plane
        bpy.ops.mesh.primitive_plane_add(size=self.size, enter_editmode=False)
        bpy.ops.transform.resize(value=(width, height, 1))
        bpy.ops.object.transform_apply(scale=True)

        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.subdivide(number_cuts=self.subdivisions)
        bpy.ops.object.mode_set(mode="OBJECT")
        
        bpy.ops.object.mode_set(mode="OBJECT")
        
        plane = bpy.context.object

        # Create armature and bones
        bpy.ops.object.armature_add(enter_editmode=True)

        # Delete
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.armature.delete()

        armature = bpy.context.object
        bpy.context.view_layer.objects.active = armature

        # Define the corners and midpoints
        bb_corners = [plane.matrix_world @ mathutils.Vector(corner) for corner in plane.bound_box]

        top_left = bb_corners[3]
        bottom_left = bb_corners[0]
        mid_left = (top_left + bottom_left) / 2
        top_right = bb_corners[7]
        bottom_right = bb_corners[4]
        mid_right = (top_right + bottom_right) / 2
        top_middle = (top_left + top_right) / 2
        bottom_middle = (bottom_left + bottom_right) / 2

        tail = mathutils.Vector((self.size * self.bone_length, 0, 0))
        top = mathutils.Vector((0, self.size * self.bone_length, 0))

        self.create_bone(armature, "top_left", top_left, top_left + tail)
        self.create_bone(armature, "mid_left", mid_left, mid_left + tail)
        self.create_bone(armature, "bottom_left", bottom_left, bottom_left + tail)
        self.create_bone(armature, "top_right", top_right, top_right - tail)
        self.create_bone(armature, "mid_right", mid_right, mid_right - tail)
        self.create_bone(armature, "bottom_right", bottom_right, bottom_right - tail)
        self.create_bone(armature, "top_middle", top_middle, top_middle - top)
        self.create_bone(armature, "bottom_middle", bottom_middle, bottom_middle + top)


        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        plane.select_set(True)
        armature.select_set(True)
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')

        return {'FINISHED'}

    def create_bone(self, armature, name, head, tail):
        bone = armature.data.edit_bones.new(name)
        bone.head = head
        bone.tail = tail


def add_object_button(self, context):
    self.layout.operator(
        ArmaturedPlane.bl_idname,
        text="Plane with Armature",
        icon='MESH_PLANE'
    )


def menu_func(self, context):
    self.layout.operator(ArmaturedPlane.bl_idname)


def register():
    bpy.utils.register_class(ArmaturedPlane)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(ArmaturedPlane)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
