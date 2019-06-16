<template>
      <div class="progress" :data-percentage="roundUp">
      <span class="progress-left">
        <span class="progress-bar"></span>
      </span>
      <span class="progress-right">
        <span class="progress-bar"></span>
      </span>
      <div class="progress-value">
        <div>
          {{percent}}%
          <!-- <span>completed</span> -->
        </div>
      </div>
    </div>
</template>

<script>
export default {
name: 'CircleProgress',
props:[
  'percent'
],
computed:{
  roundUp: function() {
  return 10 * Math.round(this.percent/10)
  }
}};
</script>

<style lang="scss" scoped>

//styling
$borderWidth: 7px;
$animationTime: 1.5s;
$border-color-default: #eee;
$border-color-fill: #7A9E9F;
$size: 150px;

//Create how many steps
$howManySteps: 10; //this needs to be even. 
//for fun try using 20 and changine in the HTML the data-percentage to 15 or 85

.progress {
  width: $size;
  height: $size;
  line-height: $size;
  background: none;
  margin: 0 auto;
  box-shadow: none;
  position: relative;
  &:after {
    content: "";
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: $borderWidth solid $border-color-default;
    position: absolute;
    top: 0;
    left: 0;
  }
  > span {
    width: 50%;
    height: 100%;
    overflow: hidden;
    position: absolute;
    top: 0;
    z-index: 1;
  }
  .progress-left {
    left: 0;
  }
  .progress-bar {
    width: 100%;
    height: 100%;
    background: none;
    border-width: $borderWidth;
    border-style: solid;
    position: absolute;
    top: 0;
    border-color: $border-color-fill;
  }
  .progress-left .progress-bar {
    left: 100%;
    border-top-right-radius: ($size/2);;
    border-bottom-right-radius: ($size/2);;
    border-left: 0;
    -webkit-transform-origin: center left;
    transform-origin: center left;
    //animation: loading-2 1.5s linear forwards 1.8s;
  }
  .progress-right {
    right: 0;
    .progress-bar {
      left: -100%;
      border-top-left-radius: ($size/2);;
      border-bottom-left-radius: ($size/2);;
      border-right: 0;
      -webkit-transform-origin: center right;
      transform-origin: center right;
      //animation: loading-1 1.8s linear forwards;
    }
  }
  .progress-value {
    display: flex;
    border-radius: 50%;
    font-size: 36px;
    text-align: center;
    line-height: 10px;
    margin-left: 25px;
    align-items: center;
    justify-content: center;
    height: 100%;
  }
}

/* This for loop creates the 	necessary css animation names 
Due to the split circle of progress-left and progress right, we must use the animations on each side. 
*/
@for $i from 1 through $howManySteps {
	$stepName: ($i*(100 / $howManySteps));

	//animation only the left side if below 50%
	@if $i <= ($howManySteps/2) { 
		.progress[data-percentage="#{$stepName}"] {
			.progress-right .progress-bar {
				 animation: loading-#{$i} $animationTime linear forwards;
			}
			.progress-left .progress-bar {animation: 0;}
		}
	}
	//animation only the right side if above 50%
	@if $i > ($howManySteps/2)  {  
		.progress[data-percentage="#{$stepName}"] {
			.progress-right .progress-bar {
				animation: loading-#{($howManySteps/2)} $animationTime linear forwards; //set the animation to longest animation
			}
			.progress-left .progress-bar {
      animation: loading-#{$i - ($howManySteps/2)} $animationTime linear forwards $animationTime;
    }
		}
	}
}

//animation
@for $i from 1 through ($howManySteps/2) { 
	$degrees: (180/($howManySteps/2));
	$degrees: ($degrees*$i);
	@keyframes loading-#{$i}{
    0%{
        -webkit-transform: rotate(0deg);
        transform: rotate(0deg);
    }
    100%{
        -webkit-transform: rotate($degrees);
			transform: rotate(#{$degrees}deg);
    }
	}
}
//additional styling
.progress {
		margin-bottom: 1em;
	}
</style>
