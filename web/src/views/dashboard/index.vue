<template>
  <div class="dashboard-container">
    <div class="vertical-align">
      <el-upload
        action
        class="avatar-uploader"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
        :on-change="handleChange"
        list-type="picture"
        :limit="1"
        :file-list="fileList"
      >
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
    </div>
    <div class="vertical-align">
      <el-form
        ref="ruleForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="主体词" prop="object">
          <el-input v-model="ruleForm.objectword" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="prompt" prop="prompt">
          <el-input v-model="ruleForm.prompt" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="inpaint()" v-loading.fullscreen.lock="fullscreenLoading">生成</el-button>
          <el-button @click="resetForm()">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="dashboard-container">
      <el-row :gutter="100">
        <el-col :span="12">
          <div class="vertical-align">
            <label class="image-label">商品主体</label>
            <img class="image" :src="productUrl" alt="Product Image" />
          </div>
        </el-col>
        <el-col :span="12">
          <div class="vertical-align">
            <label class="image-label">生成结果</label>
            <img class="image" :src=generatedImageUrl alt="Generated Image" />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Dashboard',
  data() {
    return {
      imageUrl: '',
      imgKey: "",
      imagefile: null,
      ruleForm: {
        objectword: '',
        prompt: '',
      },
      rules: {
        object: [{ required: true, message: 'Subject is required', trigger: 'blur' }],
        prompt: [{ required: true, message: 'Generated Prompt is required', trigger: 'blur' }],
      },
      fullscreenLoading: false,
      fileList: [],
      productUrl: "http://10.81.196.25:5000/image/white.png",
      generatedImageUrl: "http://10.81.196.25:5000/image/white.png",
    };
  },
  mounted() {
    console.log("mount")
  },
  computed: {

  },
  methods: {
    handleAvatarSuccess(response, file) {
      this.imageUrl = file.url;
      this.imagefile = file;
    },
    uploadImage(file) {
      const formData = new FormData();
      formData.append('file', file.raw);

      axios.post('http://10.81.196.25:5000/upload', formData)
        .then(response => {
          console.log('Image uploaded successfully:', response);
          // Handle the response as needed
        })
        .catch(error => {
          console.error('Error uploading image:', error);
          // Handle the error as needed
        });
    },
    inpaint(){
      var formData = new FormData()
      formData.append('threshold', 0.3)
      formData.append('prompt', this.ruleForm.prompt)
      formData.append('dinoprompt', this.ruleForm.object)
      var that = this
      this.fullscreenLoading = true
      axios.post('http://10.81.196.25:5000/inpaint', formData)
        .then(response => {
          console.log('Image inpaint successfully:', response);
          setTimeout(() => {
            console.log('end sleep');
            that.generatedImageUrl =  "http://10.81.196.25:5000/image/" + response.data + ".png"
            that.productUrl = "http://10.81.196.25:5000/image/" + response.data + "_object.png"
            that.fullscreenLoading = false
          }, 1000);
          // Handle the response as needed
        })
        .catch(error => {
          console.error('Error uploading image:', error);
          that.fullscreenLoading = false
          // Handle the error as needed
        });
    },
    resetForm() {
      this.ruleForm = {
        objectword: '',
        prompt: '',
      }
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isPNG = file.type === 'image/png';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG && !isPNG) {
        this.$message.error('Only JPG/PNG files are allowed.');
      }
      if (!isLt2M) {
        this.$message.error('Image must be smaller than 2MB.');
      }

      return (isJPG || isPNG) && isLt2M;
    },
    handleChange(file, fileList) {
      if (file.raw) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageUrl = e.target.result;
        };
        reader.readAsDataURL(file.raw);
        this.uploadImage(file);
      }
      this.fileList = fileList;
    },
  },
};
</script>

<style lang="scss" scoped>
.dashboard-container {
  margin: 30px;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}

#image_block {
  float: left;
  margin-left: 10px;
  margin-top: 10px;
  border: 1px solid grey;
}

#image_block:hover {
  background-color: #eaeaea;
}

.dashboard-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.vertical-align {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.image-label {
  font-weight: bold;
  margin-bottom: 10px;
}

.image {
  width: 200px;
  height: 200px;
}
</style>
