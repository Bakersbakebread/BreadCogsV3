<template>
  <div>
      <card
        class="card-user"
        :style="{ borderLeft : 'solid 4px rgb(' + getRGBValues(x.member.color) + ')'}"
      >
        <div>
          <img class="img-thumbnail" :src="x.member.avatar" style="width:100px">
          <h3 class="title mt-1 mb-0 pb-0">{{x.member.name}}#{{x.member.discriminator}}</h3>
          <div class="row">
            <div class="col">
              <small>{{x.member.id}}</small>
            </div>
            <div class="col">
              <h6 class="mb-1">created<small> {{x.member.created_at | moment("from")}}</small></h6>
               {{x.member.created_at}}<br>
              
             
            </div>
          </div>
          <hr>
          <h5 class="mb-0 font-weight-bolder">Guild</h5>
          <div class="row">
            <div class="col">{{x.member.guild.name}} <small>{{x.member.guild.id}}</small></div>

            <div class="col">
              <h6 class="mb-2">JOINED <small>{{x.member.joined_at | moment("from")}}</small></h6>
              {{x.member.joined_at }}<br>
              
            </div>
          </div>
          <div v-if="x.member.roles.length > 0" class="row mt-2">
            <div class="col">
              <h6>ROLES</h6>
              <div v-for="(role, index) in x.member.roles" :key="index">
                <span
                  class="role-color"
                  :style="{ backgroundColor : 'rgb(' + getRGBValues(role.color) + ')'}"
                ></span>
                <span class="role-name">{{role.name}}</span> -
                <small>{{role.id}}</small>
              </div>
            </div>
          </div>
        </div>
      </card>
  </div>
</template>

<script>
export default {
  name: "MemberCard",
  props: ['x'],
  methods:{
        getRGBValues(str) {
      var vals = str
        .substring(str.indexOf("(") + 1, str.length - 1)
        .split(", ");
      return `${vals[0]}, ${vals[1]}, ${vals[2]}`;
    }
  }
};
</script>

<style>
</style>
