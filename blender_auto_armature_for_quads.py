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

    width: bpy.props.FloatProperty(name="Width", default=2.0, min=0.1)
    height: bpy.props.FloatProperty(name="Height", default=2.0, min=0.1)

    def execute(self, context):
        # Create a plane
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False)
        plane = bpy.context.object
        plane.scale = (self.width / 2, self.height / 2, 1)

        # Create armature and bones
        bpy.ops.object.armature_add(enter_editmode=False)
        armature = bpy.context.object
        armature.name = "Quad_Armature"
        bpy.context.view_layer.objects.active = armature

        # Set armature to edit mode to add bones
        bpy.ops.object.mode_set(mode='EDIT')
        armature = armature.data

        # Define the corners and midpoints
        top_left = mathutils.Vector((-self.width / 2, self.height / 2, 0))
        mid_left = mathutils.Vector((-self.width / 2, 0, 0))
        bottom_left = mathutils.Vector((-self.width / 2, -self.height / 2, 0))

        top_right = mathutils.Vector((self.width / 2, self.height / 2, 0))
        mid_right = mathutils.Vector((self.width / 2, 0, 0))
        bottom_right = mathutils.Vector((self.width / 2, -self.height / 2, 0))

        self.create_bone(armature, "top_left", top_left)
        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Parent the plane to the armature
        # modifier = plane.modifiers.new(name="Armature", type='ARMATURE')
        # modifier.object = armature
        # plane.parent = armature

        return {'FINISHED'}

    def create_bone(self, armature, name, head):
        bone = armature.edit_bones.new(name)
        bone.head = head
        bone.tail = head + mathutils.Vector((-0.1, 0, 0))



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
