function ValidatorGroup(validators, redisplay_function) {
    validators.forEach($.proxy(function (validator, index) {
        this.validators.push(validator);
        //noinspection JSPotentiallyInvalidUsageOfThis
        this.is_validated.push(false);
        validator.observer = this;
        validator.index = index;
    }), this);
    this.real_redisplay_func = redisplay_function;
    this.redisplay = function () {
        this.real_redisplay_func(this.is_all_validated());
    };
}
ValidatorGroup.prototype = {
    validators: [],
    is_validated: [],
    is_all_validated: function () {
        var ret = true;
        this.is_validated.forEach(function (is_this_validate) {
            ret = ret && is_this_validate;
        });
        return ret;
    },
    validate: function (index) {
        this.validators[index].validate();
    }
};
function Validator(csrf_token, the_obj, after_validate_fun, url_to_send_value_to, send_when_validate, custom_validate_func) {
    this.csrf_token = csrf_token;
    this.the_object = the_obj;
    this.after_validate = after_validate_fun;
    this.url_to_send_value_to = url_to_send_value_to;
    this.send_when_validate = send_when_validate;
    this.custom_validate_func = custom_validate_func;
    this.ajax_id = 0;
}
Validator.prototype = {
    observer: null,
    index: -1,
    validate: function () {
        /*控件为空，认为验证失败*/
        if (this.the_object.val() == "") {
            if (this.after_validate != null) {
                this.after_validate(false);
            }
            this.observer.is_validated[this.index] = false;
            this.observer.redisplay();
            return;
        }
        if (!(this.custom_validate_func != null && !this.custom_validate_func())) {
            if (this.custom_validate_func != null && this.custom_validate_func() && this.url_to_send_value_to == null) {
                /*用户提供的验证函数成功*/
                if (this.after_validate != null) {
                    this.after_validate(true);
                }
                this.observer.is_validated[this.index] = true;
                this.observer.redisplay();
                return;
            }
        } else {
            /*用户提供的验证函数失败*/
            if (this.after_validate != null) {
                this.after_validate(false);
            }
            this.observer.is_validated[this.index] = false;
            this.observer.redisplay();
            return;
        }
        /*序列化控件*/
        var to_post = [
            {name: "csrfmiddlewaretoken", value: this.csrf_token},
            {name: this.the_object.attr("name"), value: this.the_object.val()},
            {name: "ajax_id", value: ++this.ajax_id}
        ];
        /*序列化附加控件*/
        if (this.send_when_validate != null) {
            var i;
            for (i = 0; i < this.send_when_validate.length; ++i) {
                to_post[to_post.length] = {
                    name: this.send_when_validate[i].attr("name"),
                    value: this.send_when_validate[i].val()
                };
            }
        }
        function ajax_validate(ret) {
            //noinspection JSPotentiallyInvalidUsageOfThis
            if (ret.ajax_id != this.ajax_id) {
                return;
            }
            //noinspection JSUnresolvedVariable
            var is_success = ret.is_valid;
            //noinspection JSPotentiallyInvalidUsageOfThis
            if (this.after_validate != null) {
                //noinspection JSPotentiallyInvalidUsageOfThis
                this.after_validate(is_success);
            }
            //noinspection JSPotentiallyInvalidUsageOfThis
            this.observer.is_validated[this.index] = is_success;
            //noinspection JSPotentiallyInvalidUsageOfThis
            this.observer.redisplay();
        }

        if (this.url_to_send_value_to != null) {
            $.post(this.url_to_send_value_to, to_post, $.proxy(ajax_validate, this));
        }
    }
};