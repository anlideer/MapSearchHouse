<template>
<div>
  <br/><br/><br/>
<div class='login-form'>
  <a-form layout="inline" :form="form" @submit="handleSubmit">
    <a-form-item :validate-status="userNameError() ? 'error' : ''" :help="userNameError() || ''">
      <a-input
        v-decorator="[
          'userName',
          { rules: [{ required: true, message: 'Please input your username!' }] },
        ]"
        placeholder="Username"
      >
        <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-item>
    <br/><br/>
    <a-form-item :validate-status="passwordError() ? 'error' : ''" :help="passwordError() || ''">
      <a-input
        v-decorator="[
          'password',
          { rules: [{ required: true, message: 'Please input your Password!' }] },
        ]"
        type="password"
        placeholder="Password"
      >
        <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-item>
    <br/><br/>
    <a-form-item class='login-btn'>
      <a-button type="primary" html-type="submit" :disabled="hasErrors(form.getFieldsError())">
        登录
      </a-button>
    </a-form-item>
    <div>没有账号？<router-link to='/register'>注册</router-link></div>
  </a-form>
</div>
</div>
</template>

<script>
function hasErrors(fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field]);
}
export default {
  data() {
    return {
      hasErrors,
      form: this.$form.createForm(this, { name: 'horizontal_login' }),
    };
  },
  mounted() {
    this.$nextTick(() => {
      // To disabled submit button at the beginning.
      this.form.validateFields();
    });
  },
  methods: {
    // Only show error after a field is touched.
    userNameError() {
      const { getFieldError, isFieldTouched } = this.form;
      return isFieldTouched('userName') && getFieldError('userName');
    },
    // Only show error after a field is touched.
    passwordError() {
      const { getFieldError, isFieldTouched } = this.form;
      return isFieldTouched('password') && getFieldError('password');
    },
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          // 在这里接登录接口
          this.$axios({
            url: 'http://182.92.223.235:8888/login',
            method: 'post',
            data: {
              'username': values.userName,
              'password': this.$md5(values.password)
            }
          }).then(res => {
            console.log(res.data);
            if (res.data['code'] == 200){
              this.$message.success('登录成功');
              this.$router.push({name: 'home'});
            }
            else if (res.data['code'] == 10001){
              this.$message.error('密码错误或账户不存在');
            }
            else 
            {
              this.$message.error('登录失败');
            }
          }).catch(e)
          {
            console.log(e);
          }
        }
      });
    },
  },
};
</script>

<style lang='less' scoped>
.login-form {
  margin-left: 600px;
  margin-top: 100px;
  height: 200px;
  width: 400px;
}
.login-btn {
  margin-left: 50px;
}
</style>