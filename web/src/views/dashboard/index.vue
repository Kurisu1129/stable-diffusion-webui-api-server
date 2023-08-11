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
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="主体词" prop="object">
          <el-input v-model="ruleForm.object" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="prompt" prop="prompt">
          <el-input v-model="ruleForm.prompt" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="inpaint()">生成</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="dashboard-container">
      <el-row>
        <el-col :span="24">
          <div class="vertical-align">
            <label class="image-label">Product Image</label>
            <img class="image" :src="productUrl" alt="Product Image" />
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="vertical-align">
            <label class="image-label">Generated Image</label>
            <img class="image" :src="output" alt="Generated Image" />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import output from '../../../../service/image/output/output.png'
export default {
  name: 'Dashboard',
  data() {
    return {
      imageUrl: '',
      imgKey: "",
      imagefile: null,
      ruleForm: {
        object: '',
        prompt: '',
      },
      output,
      rules: {
        object: [{ required: true, message: 'Subject is required', trigger: 'blur' }],
        prompt: [{ required: true, message: 'Generated Prompt is required', trigger: 'blur' }],
      },
      fileList: [],
      productUrl: '',
      generatedImageUrl: '../../assets/white.png',
    };
  },
  mounted() {
    console.log("mount")
  },
  methods: {
    handleAvatarSuccess(response, file) {
      this.imageUrl = file.url;
      this.imagefile = file;
    },
    uploadImage(file) {
      const formData = new FormData();
      formData.append('file', file.raw);

      axios.post('http://127.0.0.1:5000/upload', formData)
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
      axios.post('http://127.0.0.1:5000/inpaint', formData)
        .then(response => {
          console.log('Image inpaint successfully:', response);
          this.generatedImageUrl = '../../../../service/image/output/output.png'
          // Handle the response as needed
        })
        .catch(error => {
          console.error('Error uploading image:', error);
          // Handle the error as needed
        });
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
  width: 300px;
  height: 160px;
}
</style>
