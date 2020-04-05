

/*
Gallery_recommend_big
轮播图设计
    -点击4个小点切换
    -setInterval定时器自动轮播
    -上一张/下一张切换

 （待优化：当前小点颜色切换使用class=active，再在css样式表中对active进行样式渲染，去颜色的话就删除这个class=active属性）
 */

//定义全局变量和方法
//children只返回节点下面的html元素节点，不返回一些文本节点



//获取图片列表和小点列表对象
var slide_trigger=document.getElementById('slide_trigger').children;
var recommend_slide=document.getElementById('recommend_slide').children;
var pre_pic_btn=document.getElementById('left_trigger');
var nex_pic_btn=document.getElementById('right_trigger');


//定义一个全局的轮播图（正在、希望）跳转的图和小点的索引
var c_index=0;

//定义一个更换图片的方法，接收参数为希望跳转的图片和小点的索引
var change_picture=function(ind){
        document.querySelector(".active_pic").className='recommend_big_item';
        // 接收希望跳转的索引参数，将对应的图片对象的class值添加上active_pic
        recommend_slide[ind].className+=' active_pic';

}

//定义一个更换小点颜色的方法，接收参数为希望跳转的图片和小点的索引
var change_dot=function(ind){
        //将之前标记为active_dot的小点的的class值恢复成默认; 注意这里寻找active_dot的是会变的对象，不能将它赋值给一个变量；
        document.querySelector(".active_dot").className='dot';
        //把选中的小点对象的class值添加上active_dot
        slide_trigger[ind].className+=' active_dot';


}

//-点击4个小点切换
//(第一层for 为每个小点注册onclick函数，并且每次循环为每个小点添加index属性来保存当前循环的索引值
for(let c=0;c<slide_trigger.length;c++){
// 保存当前对象的索引:由于for循环内的事件函数是在循环结束后，事件发生时才运行的；所以现在每次循环元素对象的时候，给元素对象贴上index标签
    slide_trigger[c].index=c;
    slide_trigger[c].onclick=function(){
        //将用户所点击的小点的index赋值给全局的c_index索引变量；
        c_index=this.index;
        change_picture(c_index);
        change_dot(c_index);
        c_index=this.index;
    }

}

// setInterval定时器自动轮播
// 定义一个轮播图函数
function autochange(){
        c_index++;
        if(c_index==4){
            c_index=0;
            }
        console.log(c_index);
        change_picture(c_index);
        change_dot(c_index);

}

// 创建一个定时器开启计时，传入轮播图函数，每4秒就会执行这个函数
var auto_picture=setInterval(autochange, 4000);
var gallery_recommend_big=document.getElementById('gallery_recommend_big');

//鼠标移入的时候清除定时器
gallery_recommend_big.onmouseover=function(){
    console.log('timer stop');
    clearInterval(auto_picture);


};

//鼠标移出的时候重启定时器
gallery_recommend_big.onmouseout=function(){
    console.log('timer restart');
    auto_picture=setInterval(autochange, 4000);

};


//-上一张/下一张切换

pre_pic_btn.onclick=function(){
    c_index--;
    if(c_index<0){
        c_index=3;
        };
    change_picture(c_index);
        change_dot(c_index);
}

nex_pic_btn.onclick=function(){
    c_index++;
        if(c_index==4){
            c_index=0;
            }
    change_picture(c_index);
        change_dot(c_index);
}





