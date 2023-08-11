from PIL import Image
import webuiapi

image = Image.open("./image/upload/00027-3992057090.png")
api = webuiapi.WebUIApi(host='175.178.168.6', port=8081)

def hello_world():
    return "<p>Hello, World!</p>"

def sam_init():
    b64Img = webuiapi.b64_img(image)
    params = {
        "input_image": b64Img,
        "dino_model_name": "GroundingDINO_SwinT_OGC (694MB)",
        "text_prompt": "a cat",
        "box_threshold": 0.3
    }
    #samResult = api.post_and_get_api_result("http://175.178.168.6:8081/sam/dino-predict", params, False)
    samResult = api.dino_to_map_result(api.session.post(url="http://175.178.168.6:8081/sam/dino-predict", json=params, timeout=65535))
    samResult["image"].save(f'./image/sam.png')
    return 

def sam_init_with_dino(threshold):
    b64Img = webuiapi.b64_img(image)
    params = {
        "sam_model_name": "sam_vit_h_4b8939.pth",
        "input_image": b64Img,
        "sam_positive_points": [],
        "sam_negative_points": [],
        "dino_enabled": True,
        "dino_model_name": "GroundingDINO_SwinT_OGC (694MB)",
        "dino_text_prompt": "a bottle",
        "dino_box_threshold": threshold,
        "dino_preview_checkbox": False,
        "dino_preview_boxes_selection": [
          0
        ]
    }
    samResult = api.sam_to_map_result(api.session.post(url="http://175.178.168.6:8081/sam/sam-predict", json=params, timeout=65535))
    samResult["image"].save(f'./image/sam_dino.png')
    return 

def inpaint(dinoThreshold, prompt):
    # sam图像分割
    sam_init_with_dino(dinoThreshold)
    # 重绘
    mask = Image.open("./image/sam_dino.png")
    inpainting_result = api.img2img(images=[image],
                                mask_image=mask,
                                inpainting_fill=1,
                                prompt=prompt,
                                seed=104,
                                cfg_scale=5.0,
                                denoising_strength=0.7,
                                use_async=False)
    inpainting_result.image.save(f'./image/output/output.png')
    return "success"