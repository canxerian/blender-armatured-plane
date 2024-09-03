import bpy
import mathutils

bl_info = {
    "name": "Auto Armature for Quads",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Adds an armature with bones to 2D quads",
    "author": "Mark Nguyen",
    "version": (1, 0, 0),
    "doc_url": "https://github.com/canxerian/blender-auto-armature-for-quads",
    "location": "View3D > Add > Mesh > Quad with Armature"
}


class AutoArmatureForQuads(bpy.types.Operator):
    """Add bones to a quad"""
    bl_idname = "mesh.auto_armature_quad"
    bl_label = "Quad with Armature"
    bl_options = {'REGISTER', 'UNDO'}

    size: bpy.props.FloatProperty(name="Size", default=2.0, min=0.1)
    width: bpy.props.FloatProperty(name="Width", default=2.0, min=0.1)
    height: bpy.props.FloatProperty(name="Height", default=2.0, min=0.1)
    subdivisions: bpy.props.IntProperty(name="Subdivisions", default=2, min=1)
    
    def execute(self, context):
        # Create a plane
        bpy.ops.mesh.primitive_plane_add(size=self.size, enter_editmode=False, scale=mathutils.Vector((self.width, self.height, 1)))
        plane = bpy.context.object

        # Create armature and bones
        bpy.ops.object.armature_add(enter_editmode=True)

        # Delete
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.armature.delete()

        armature = bpy.context.object
        armature.name = "Quad_Armature"
        bpy.context.view_layer.objects.active = armature

        # Define the corners and midpoints
        bb_corners = [plane.matrix_world @ mathutils.Vector(corner) for corner in plane.bound_box]

        top_left = bb_corners[3]
        bottom_left = bb_corners[0]
        mid_left = (top_left + bottom_left) / 2
        
        top_right = bb_corners[7]
        bottom_right = bb_corners[4]
        mid_right = (top_right + bottom_right) / 2

        tail = mathutils.Vector((self.size * 0.2, 0, 0))

        self.create_bone(armature, "top_left", top_left + tail, top_left)
        self.create_bone(armature, "mid_left", mid_left + tail, mid_left)
        self.create_bone(armature, "bottom_left", bottom_left + tail, bottom_left)
        self.create_bone(armature, "top_right", top_right - tail, top_right)
        self.create_bone(armature, "mid_right", mid_right - tail, mid_right)
        self.create_bone(armature, "bottom_right", bottom_right - tail, bottom_right)


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
        AutoArmatureForQuads.bl_idname,
        text="Quad with Armature",
        icon='MESH_PLANE'
    )


def menu_func(self, context):
    self.layout.operator(AutoArmatureForQuads.bl_idname)


def register():
    bpy.utils.register_class(AutoArmatureForQuads)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(AutoArmatureForQuads)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
