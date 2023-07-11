<!-- eslint-disable indent -->
<template>
  <div class="dashboard-container">
    <div>
      <el-upload
        action="https://jsonplaceholder.typicode.com/posts/"
        class="avatar-uploader"
        :show-file-list="false"
        :on-success="handleAvatarSuccess"
        list-type="picture"
        :limit="1"
      >
        <img v-if="imageUrl" :src="imageUrl" class="avatar"/>
        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
    </div>
    <div>
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="主体词" prop="pass">
          <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="生成prompt" prop="checkPass">
          <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">生成</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="infinite-list" v-infinite-scroll="loadImage" style="overflow:auto;height: 900px">
      <div id="image_block"
           v-for="each_image of image_list"
           :key=each_image.id
      >
        <img :src="each_image.url" alt="no" width="300px" height="160px">
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      url: '"https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      imageUrl: '',
      ruleForm: {
        pass: '',
        checkPass: '',
        age: ''
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
      fileList: []
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
    // axios.post("/api/search_image", formdata).then(this.handleUploadSucc);
  },
  methods: {
    handleAvatarSuccess(res, file) {
      this.imageUrl = file.url
    },
    loadImage() {
      this.cur_index += this.page_size
      var formdata = new FormData()
      formdata.append('start', this.cur_index)
      formdata.append("limit", this.page_size)
      formdata.append("file_class", "0")
      // axios.post("/api/search_image", formdata).then(this.handleUploadSucc)
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
</style>

