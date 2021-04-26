<template>
<div>
  <br/><br/><br/><br/>
  <div class='form-register'>
  <a-form :form="form" @submit="handleSubmit">
    <a-form-item v-bind="formItemLayout" label="UserName">
      <a-input
        v-decorator="[
          'userName',
          {
            rules: [
              {
                required: true,
                message: 'Please input your user name!',
              },
            ],
          },
        ]"
      />
    </a-form-item>
    <a-form-item v-bind="formItemLayout" label="Password" has-feedback>
      <a-input
        v-decorator="[
          'password',
          {
            rules: [
              {
                required: true,
                message: 'Please input your password!',
              },
              {
                validator: validateToNextPassword,
              },
            ],
          },
        ]"
        type="password"
      />
    </a-form-item>
    <a-form-item v-bind="formItemLayout" label="Confirm Password" has-feedback>
      <a-input
        v-decorator="[
          'confirm',
          {
            rules: [
              {
                required: true,
                message: 'Please confirm your password!',
              },
              {
                validator: compareToFirstPassword,
              },
            ],
          },
        ]"
        type="password"
        @blur="handleConfirmBlur"
      />
    </a-form-item>
    <a-form-item v-bind="tailFormItemLayout" class='register-btn'>
      <a-button type="primary" html-type="submit">
        注册
      </a-button>
    </a-form-item>
  </a-form>
  </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      confirmDirty: false,
      // residences,
      autoCompleteResult: [],
      formItemLayout: {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 8 },
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 16 },
        },
      },
      tailFormItemLayout: {
        wrapperCol: {
          xs: {
            span: 24,
            offset: 0,
          },
          sm: {
            span: 16,
            offset: 8,
          },
        },
      },
    };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: 'register' });
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFieldsAndScroll((err, values) => {
        if (!err) {
          // 在这里接注册接口
          this.$axios({
            url: 'http://182.92.223.235:8888/register',
            method: 'post',
            data: {
              'username': values.userName,
              'password': this.$md5(values.password)
            }
          }).then(res => {
            console.log(res.data);
            if (res.data['code'] == 200)
            {
              this.$message.success('注册成功');
              this.$router.push({name: 'login'});
            }
            else if (res.data['code'] == 10001)
            {
              this.$message.warning('用户名已被占用');
            }
            else 
            {
              this.$message.error('注册失败');
            }
          }).catch(e)
          {
            console.log(e);
          }
        }
      });
    },
    handleConfirmBlur(e) {
      const value = e.target.value;
      this.confirmDirty = this.confirmDirty || !!value;
    },
    compareToFirstPassword(rule, value, callback) {
      const form = this.form;
      if (value && value !== form.getFieldValue('password')) {
        callback('Two passwords that you enter is inconsistent!');
      } else {
        callback();
      }
    },
    validateToNextPassword(rule, value, callback) {
      const form = this.form;
      if (value && this.confirmDirty) {
        form.validateFields(['confirm'], { force: true });
      }
      callback();
    },

  },
};
</script>

<style lang='less' scoped>
.form-register {
  width: 500px;
  margin-top: 50px;
  margin-left: 500px;
}
.register-btn {
  margin-left: 180px;
}
</style>