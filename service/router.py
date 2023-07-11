from PIL import Image
import webuiapi

image = Image.open("D:/Users/evans01.chen/Downloads/423b6eb6-1b5b-44cc-8bc9-d493dd996284.jpg")
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
    samResult = api._to_map_result(api.session.post(url="http://175.178.168.6:8081/sam/dino-predict", json=params, timeout=65535))
    samResult.image.save(f'./image/sam.png')
    return 

def inpaint():
    # 暂时声明
    mask = image
    inpaintPrompt = "cute cat"
    inpainting_result = api.img2img(images=[image],
                                mask_image=mask,
                                inpainting_fill=1,
                                prompt=inpaintPrompt,
                                seed=104,
                                cfg_scale=5.0,
                                denoising_strength=0.7,
                                use_async=False)
    inpainting_result.image.save(f'./image/1.png')
    return "success"