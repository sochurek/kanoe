<script>

        var formAjaxValidate = document.getElementById("form");

        var checkForm = function(e) {

          var form = e.target;




          if(this.name.value == "") {
            alert("Prosím zadejte přezdívku!");
            this.name.focus();
            e.preventDefault();
            return;
        
          }



          $
          $.ajax({
            type: "POST",
            url: "/api/check-name/" + this.name.value
          });


          
          if(this.email.value == "" || !this.valid_email.checked) {
            alert("Please enter a valid Email address");
            this.email.focus();
            e.preventDefault();
            return;
          }

          if(this.age.value == "" || !this.valid_age.checked) {
            alert("Please enter an Age between 16 and 100");
            this.age.focus();
            e.preventDefault();
            return;
          }
          
          e.preventDefault();
        }

      formAjaxValidate.addEventListener("submit", checkForm, false);

      formAjaxValidate.name.addEventListener("change", function(e) {
      this.value = this.value.replace(/^\s+|\s+$/g, "");
      this.form.valid_name.checked = this.value;
      }, false);

      formAjaxValidate.email.addEventListener("change", function(e) {
      if(this.value != "") {
      callAjax("checkEmail", this.value, this.id);
      }
      }, false);

      formAjaxValidate.age.addEventListener("keyup", function(e) {
      if(this.value != "") {
      callAjax("checkAge", this.value, this.id);
      }
      }, false);


    </script>