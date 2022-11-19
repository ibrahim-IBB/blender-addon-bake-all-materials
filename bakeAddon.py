import bpy




bl_info = {
    "name": "bakeAllMaterial",
    "blender": (3, 3, 1),
    "category": "Material",
}


TextureName="MainTexture"
def create_image(name,width,height):
    
    if bpy.data.images.get(name) is None:
        
        data=bpy.data.images.new(name=name,width=width,height=height)
        return data
    else:
        data=bpy.data.images.get(name)
        return data

def remove_image(name):
    
    image=bpy.data.images.get(name)
    if image:
        
        bpy.data.images.remove(image)
    


                    
                    


class BakeOperator(bpy.types.Operator):
    bl_idname="node.bake_all_materials"
    bl_label="bake_all_materials"
    
    image_width:bpy.props.IntProperty(name="image_width",default=500)
    image_height:bpy.props.IntProperty(name="image_height",default=500)
  
    
    def execute(self,context):
        
        #cleaning
        
        for slot in bpy.context.object.material_slots:
                
            #print("Material### Name:{}".format(slot.material.name))
            for node in slot.material.node_tree.nodes:
                
            #print(node)
                if(node.type=="TEX_IMAGE"):
                    
                    if node.image:
                        
                        if node.image.name==TextureName:
                            
                            slot.material.node_tree.nodes.remove(node)
                
        remove_image(TextureName)
        #recreating
        for slot in bpy.context.object.material_slots:
            
            node=slot.material.node_tree.nodes.new("ShaderNodeTexImage")
            node.location=(100,100)
            image=create_image(TextureName,width=self.image_width,height=self.image_height)
            node.image=image
            node.select=True
            print(node.image)
        
        bpy.ops.object.bake(type=bpy.context.scene.cycles.bake_type)
            
        #print("width {}".format(self.image_width))
        #print("####")
        #print("height {}".format(self.image_height))
        
        return {"FINISHED"}



class Bake_node_Panel(bpy.types.Panel):
    bl_idname="SHADER_PT_bake_panel"
    bl_label="bakeAddon"
    bl_space_type="NODE_EDITOR"
    bl_region_type="UI"
    
    def draw(self,context):
        if bpy.context.scene.render.engine=="CYCLES":
            
            layout=self.layout
            op=layout.operator("node.bake_all_materials")
            layout.prop(context.object,"Global_width",text="image width")
            layout.prop(context.object,"Global_height",text="image height")
            op.image_width=context.object.Global_width
            op.image_height=context.object.Global_height
    

classes=(BakeOperator,Bake_node_Panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Object.Global_width=bpy.props.IntProperty(name="Global_width",default=500)
    bpy.types.Object.Global_height=bpy.props.IntProperty(name="Global_height",default=500)
    



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Object.Global_width
    del bpy.types.Object.Global_height

