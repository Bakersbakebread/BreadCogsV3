<template>
  <div @mouseover="showTip = true" @mouseout="showTip = false" class="myTooltip">
    <slot name="text"></slot>
    <span v-if="showTip" id="tooltiptext">
      <slot name="tooltip"></slot>
    </span>
  </div>
</template>

<script>
export default {
  name: "tooltip",
  data() {
    return {
      showTip: false
    };
  }
};
</script>

<style>
.myTooltip {
  position: relative;
  display: inline-block;
}
.myTooltip:hover{
  cursor: pointer;
}

#tooltiptext {
  width: 200px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 5px;
  

  position: absolute;
  z-index: 9999;
  bottom: 130%;
  left: -50%;

}

</style>
