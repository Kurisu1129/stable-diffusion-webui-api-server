from PIL import Image
import webuiapi
import time
image = Image.open("./image/upload/8d6729ca-5ba3-40b9-9afe-01da5c67100c.jpg")
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

def sam_init_with_dino(threshold, dinoprompt):
    image = Image.open("../web/src/assets/image/upload/upload.png")
    b64Img = webuiapi.b64_img(image)
    params = {
        "sam_model_name": "sam_vit_h_4b8939.pth",
        "input_image": b64Img,
        "sam_positive_points": [],
        "sam_negative_points": [],
        "dino_enabled": True,
        "dino_model_name": "GroundingDINO_SwinT_OGC (694MB)",
        "dino_text_prompt": dinoprompt,
        "dino_box_threshold": threshold,
        "dino_preview_checkbox": False,
        "dino_preview_boxes_selection": [
          0
        ]
    }
    samResult = api.sam_to_map_result(api.session.post(url="http://175.178.168.6:8081/sam/sam-predict", json=params, timeout=65535))
    samResult["image"].save(f'./image/sam_dino.png')
    samResult["object"].save(f'./image/sam_dino_object.png')
    return 

def inpaint(dinoThreshold, prompt, dinoprompt):
    image = Image.open("../web/src/assets/image/upload/upload.png")
    # sam图像分割
    sam_init_with_dino(dinoThreshold, dinoprompt)
    # 重绘
    mask = Image.open("./image/sam_dino.png")
    objectImage = Image.open("./image/sam_dino_object.png")
    inpainting_result = api.img2img(images=[image],
                                mask_image=mask,
                                inpainting_fill=0,
                                prompt=prompt,
                                seed=int(time.time()),
                                cfg_scale=5.0,
                                denoising_strength=0.7,
                                inpaint_full_res_padding = 32,
                                use_async=False)
    trace = str(int(time.time()))
    inpainting_result.image.save('./image/output/' + trace + '.png')
    objectImage.save('./image/output/' + trace + '_object.png')
    return trace