<!-- eslint-disable indent -->
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
        <img v-if="imageUrl" :src="imageUrl" class="avatar"/>
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
    </div>
    <div class="vertical-align">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="主体词" prop="pass">
          <el-input v-model="ruleForm.object" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="生成prompt" prop="checkPass">
          <el-input v-model="ruleForm.prompt" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">生成</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

<div class="dashboard-container">
    <el-row>
      <el-col :span="24">
        <div class="vertical-align">
          <label class="image-label">Product Image</label>
          <img class="image" :src="productImageUrl" alt="Product Image">
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <div class="vertical-align">
          <label class="image-label">Generated Image</label>
          <img class="image" :src="generatedImageUrl" alt="Generated Image">
        </div>
      </el-col>
    </el-row>
  </div>
</div>
</template>

<script>
import {mapGetters} from 'vuex'
import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:5000';
axios.defaults.timeout = 5000;
export default {
  name: 'Dashboard',
  data() {
    return {
      url: '"https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      imageUrl: '',
      ruleForm: {
        object: '',
        prompt: ''
      },
      rules: {
        pass: [
          {trigger: 'blur'}
        ],
        checkPass: [
          {trigger: 'blur'}
        ],
        age: [
          {trigger: 'blur'}
        ]
      },
      image_list: [{id:1,url:"https://img1.baidu.com/it/u=1919509102,1927615551&fm=253&fmt=auto&app=120&f=JPEG?w=889&h=500"},
        {id:2,url:"https://img1.baidu.com/it/u=1919509102,1927615551&fm=253&fmt=auto&app=120&f=JPEG?w=889&h=500"}],
      cur_index: 0,
      page_size: 25,//每页25个
      fileList: [],
      productUrl: "",
      generatedImageUrl: ""
    }
  },
  computed: {
    ...mapGetters(['name'])
  },
  mounted() {
    var formdata = new FormData();
    formdata.append('start', 0)
    formdata.append("limit", this.page_size)
    formdata.append("file_class", "0")
    // axios.post("/inpaint", formdata).then(this.handleUploadSucc);
  },
  methods: {
    handleAvatarSuccess(response, file) {
  this.imageUrl = file.url;
  const formdata = new FormData();
  formdata.append('file', file);

  axios.post('/upload', formdata)
    .then(uploadResponse => {
      // Handle the upload response
      console.log(uploadResponse.data);
    })
    .catch(uploadError => {
      // Handle the upload error
      console.error(uploadError);
    });
},
    loadImage() {
      this.cur_index += this.page_size
      var formdata = new FormData()
      formdata.append('start', this.cur_index)
      formdata.append("limit", this.page_size)
      formdata.append("file_class", "0")
      // axios.post("/api/search_image", formdata).then(this.handleUploadSucc)
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
    }
    this.fileList = fileList;
  },
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }

  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
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
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

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

