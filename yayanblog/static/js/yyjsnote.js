/*js重点
1.sgg51-67
作用域：函数和全局
构造函数
原型链

2.数组和string方法

3.DOM和BOM


 */




/*

一.js输出语句
1.弹出框：alert('this is a alert');
2.添加到页面最后一个元素:document.write('<h1>this is document write</h1>');
3.页面控制台输出：console.log("console log text");

*/

/*
二.js编写位置
1.在html标签中添加onclick属性，直接添加js语句
（onclick 属性可以使用于所有 HTML 元素，除了 ：<base>, <bdo>, <br>, <head>, <html>, <iframe>, <meta>, <param>, <script>, <style>, 和 <title>.）

ex: <h2 onclick="alert('this is blog title')">{{ admin.blog_title  }}</h2>

2.超链接href中:href="javascript:js语句;"
ex:<a href="javascript:alert('this is a link to github')">Yayan Su</a>

3.编写入head 中<script>标签：立即执行

4.（最常使用）编写入外部js文件，在head 中用<script>标签引入（css使用link引入）
    <script type="text/javascript" src="{{ url_for('static',filename='js/yyjsnote.js')}}"></script>
5.文档加载：js如果有用到文档中的元素，则需要在文档加载完毕后那个元素才能执行；所以一般script文件放在页面尾部


 */

/*
三.js数据类型 ：typeof a 可以知道这个a的变量类型


1.String 字符串
 var s='i am string '
 转义字符：\ : \t ,\n ,\" ,\\

 //字符串方法：
    (不改变原始字符)
    -s.length：字符串的长度
    -s[9]:第10个字符
    -s.charAt(2) :返回指定索引为2的字符
    -s.slice（0,2）:和数组一样



2.Number数值 :在js中，所有数值都是number类型，包括整数和浮点数
    Number.MAX_VALUE js中最大的值
    Number.MIN_VALUE 大于0的最小正值
    infinity 正无穷
    -infinity 负无穷
    NaN 也是一个特殊的数字
    js的整数的运算基本可以保证精确，但是进行浮点运算，可能不精确0.1+0.2

3.Boolean
    true
    flase


4.Null ：表示一个为空的对象
typeof null ，返回object

5.Undefined：当声明一个变量，但未赋值

6.object对象（引用类型）


// 基本数据类型和引用数据类型的区别
1.基本数据类型 :变量名和值直接在栈内存中存储；一个变量的值的变化不会应影响别的变量（变量的赋值传递的只是值，新变量会在新的栈内存空间来保存这个值，两个值独立存在）

2.引用数据类型（对象）：
var obj=new object()
对象名存在栈内存中，创建的对象会在堆内存中开辟一个空间，将堆内存地址保存到了变量名；

所以obj2=obj，obj2收到的是obj指向的对象的堆内存地址，两个变量指向同一个对象





//类型转化:

(1)a.toString()方法,会返回新值 ; null 和undefined 不可以使用a.toString(),但可以使用String(a)函数；
(2)使用Number(a)函数；如果有非法的数字，就转换成NaN
(3)parseInt()：把一个字符串中的有效的整数数字部分提出来，转换成number
(4)Boolean(a): 除了 0 ,NaN ,'' ,null ,undefined 都是 true




 // a++和++a
 a++ 的值 是自增前的a的原始值
 ++a 的值 是自增后的a的新值
 a=20
 a++ + ++a + a = 20 + 22+ 22 = 64




 */








/*

四.对象:object ；
对象属于一种复合的数据类型，可以保存多个不同数据类型的属性；
//对象类型
内建对象：Math,String....
宿主对象：浏览器
自定义对象：自己创建的对象

 //创建对象
 （1）用new object()方式
 var obj=new object();
 （2）使用对象字面量，创建对象同时直接指定对象中属性
 var obj={属性名：属性值，属性名：属性值}
 属性名的引号可加可不加，但是如果属性名是特殊形式，必须加引号

 //添加、修改对象属性：
 对象名.属性名=属性值 或者对象名['属性名']=属性值（属性名是特殊形式或者是变量的话，必须使用这种第二种形式）



 //删除对象属性：
 delete 对象名.属性名

 //查看某个属性是否在对象中 ：in
 "属性名" in 对象名


 //用工厂方法创建对象（用的不多）
 function createobj(形参){
    var obj={
       ...
    }
    return obj;
 }
 obj1=createobj(实参);
 obj2=createobj(实参);
使用工厂方法创建的对象都是Object这个类型，导致无法五分多种不同类型的对象

 //用构造函数创建对象(重要):

1.构造函数和普通函数的区别就是调用方式不同：普通函数加（）直接调用，构造函数需要使用new关键字调用
    var yayan=new Person('yayan',18)
2.首先要先创建Person()这个构造函数，函数名首字母大写
3.构造函数的执行流程
    -立刻创建一个新的对象
    -将新建的对象设置为函数中this，在构造函数中可以使用this 来引用新建的对象
    -构造函数中不需要return
    -用同一个构造函数new出来的对象属于同一类的对象（js的构造函数很像其他语言的class）
    -用instanceof 可以检查一个对象是否是一个构造函数的实例: yayan instanceof Person (所有对象都是Object的实例)


function Person(name,age){
    this.name=name;
    this.age=age;
    this.pfun=function(){
        alert('my name is'+this.name)

    }

}
4.构造函数的方法重复创建问题：构造函数每执行一次都会创建一个新的方法，占用太大空间；可以使所有的对象共享同一个方法
    （1）将这个构造函数的方法指向全局空间已经定义好的一个函数（不推荐，污染了全局作用域的命名空间）
    （2）使用prototype原型方式

 //prototype原型：创建的每一个函数，解析器都会向函数中添加一个属性prototype
    -这个属性指向一个对象，这个对象就是所谓的原型对象；prototype>原型对象地址>原型对象
    -当函数以构造函数被new新对象的时候，它创建的对象也会有prototype这个属性 ，如果看一个对象的原型:对象名.__proto__=构造函数名.prototype
    -同一个构造函数new的所有新对象的prototype属性指向的都是同一个prototype对象
    -我们可以将所有对象共有的内容设置到这个prototype对象中
    -当我们访问一个属性，会先在自身找，如果没有，再去prototype对象中找，直到找到Object对象的原型（注意，对象的属性不会在全局作用域里找，全局作用域里的属性相当于是windows对象的属性）
    - in 和 hasOwnProperty('属性') ：
        -'属性' in 对象 会包括原型中的属性
        -对象 hasOwnProperty('属性') 检查自身的属性，不会包括原型属性


    function Person(name,age){
        this.name=name;
        this.age=age;
    }
    向构造函数的原型中添加这个公共方法
    Person.prototype.pfun=function(){
    alert('we are all person')
    }

    var yayan=new Person('yayan',18)
    所有new出来的对象都可以调用这个同一个方法，也可以重新覆盖
    yayan.pfun()

    - 用构造函数创建的对象，原型的原型就是Object对象；而直接创建的对象，上一层原型就是Object对象了




 //内建对象
 1.date
    -创建一个date对象，时间为代码执行时间：
     var cd=new Date()
    -date方法：
        cd.getday() 星期几 返回0-6
        cd.getdate() 这个月的几号
        cd.getTime() 获取这个cd的时间戳

        time=Date().now() 获取当前代码执行时的时间戳


2.Math对象:Math不是构造函数，不用创建对象，可以直接用Math.方法()/属性来调用
    -Math.PI
    -Math.abs(-1) ：绝对值
    -Math.max(1,9,...)
    -Math.ceil/floor():向上/下取整
    -Math.random() :生成一个0-1之前的随机数









 */





/*
五：函数：函数也是一个对象

 //创建一个函数对象
 (1)用new
 var fun=new Function("函数代码")

 (2)直接用function
 function 函数名(参数){
    函数代码

 }

 (3)使用函数表达式 ，用于做匿名函数
 var 函数名=function(参数){
    函数代码
 }


//函数作为对象的一个属性的值
 先定义函数：
  function fun(){
    alert('this is a fun')
 }
将函数名作为这个对象的一个属性的值（不能加括号），那么这个属性也叫做对象的方法：
 var obj={objf:fun}
调用对象的这个方法（要加括号）：
 obj.objf()


//函数对象的方法：call和apply;
    -fun.call()和fun.apply() 都是会调用这个方法
    -在调用call和apply()时，可以将一个对象指定为第一个参数，那么这个函数对象中的this就是这个对象
       ex:
       var name='globalname'
       var obj={name:'objname'}
       function name(){
        alert('my name is '+this.name)
     }
       (1)直接调用：name()> name变量是windows.name，也就是全局作用域定义的name>'globalname'
       (2)name.call/apply(obj)> name变量就是obj.name



    -call和apply不同点：
        call第一个参数为指向对象，后面依次将函数需要的实参按照位置传入call(obj,a,b)
        apply第一个参数为指向对象,第二个参数为数组，放入函数需要的实参apply(onj,[a,b])


 //函数不定数实参:arguments
    -也是浏览器传进来的隐含参数；
    -它是一个类数组对象；也可以获取长度
    -所传递的实参都会在arguments中保存，arguments的长度就是函数接收的实参数量
    function name(){
        for(var n in arguments){
         console.log(arguments[n])
        }
    }
    name('yayan','suisiu')






 */

/*
六.作用域

1.全局作用域
  -在页面打开是创建，页面关闭时销毁
  -全局作用域中有一个全部对象window
  -在全局作用域中，创建的变量都会作为window对象的属性保存 ;ex: var a=10; 等于 window.a=10


2.函数作用域

    -调用函数时创建，函数执行完毕以后，函数作用域销毁
    -函数中能访问全局作用域的变量，但是全局作用域中不能访问函数作用域
    -就近原则：如果有同名的变量，会先在自己的作用域中找这个变量
    -函数中也有声明提升的特性
    -函数中，
        不使用var声明的变量，都会去上一层找这个变量；
        只有使用var 才是声明了当前函数作用域的变量；
        如果这个函数定义了形参，就相当于在函数作用域中声明了变量，如果它没有被赋值，那么就是undefined

    -this: 解析器在调用函数每次都会向函数内部传递的一个隐含参数；this 执行一个对象，是函数执行的上下文对象；根据调用的方式不同，this会指向不同的对象；
        - 单纯调用 方法fun() ：this 就是window对象
        - 以对象的方法调用：obj.func() ,this就指向调用这个方法的obj对象
        - 当以构造函数方式new 的时候，this 就指新new出来的那个对象
        -注意：变量前要加好this才能指向正确的对象，否则默认都是window.变量


3.块作用域


4.声明提升
-使用var关键字声明的变量，会在所有代码执行之前，被提升到最前面来声明好（但是赋值行为仍然在原来地方）
-使用function 声明的函数，会在所有代码执行之前，会将函数名和它内部的代码都提升到代码最前面



 */

/*
七.数组：数组也是Object类型，只是属性名为0开始的整数

创建：var a=new Array(); 或者直接通过var a =[1,2,3]
修改/新增 ：a[0]=1;

// Array对象属性：
长度：a.length
    length可以用来cut数组


//数组的方法
（改变原始数组）
1. a.push('元素') :给数组末尾添加一个元素；返回值是数组的新的length值；unshift()是从数组头部插入
2. a.pop()：删除数组末尾元素；返回值为删除的那个元素；shift()是从数组头部删除
3. a.reverse():颠倒数组a中的元素
4. a.sort() :默认是对元素按照字符编码顺序来排序；
               可以添加一个比较函数作为参数，比较函数有两个参数a,b 依次将数组相邻元素传入；返回值<0，则会将a，b交换位置
5.a.splice(a,b,c,d...) :从索引为a的位置开始删除b个元素，并仍在索引a开始添加元素c,d...


(不会改变原始数组)
6. a.join('连接符') :将数组中的元素转成字符串并以连接符连接起来；返回值为结果字符串
7.a.slice(0,2) :提取原数组中，索引0-2（不包括2）的元素，返回值为新的数组
7.a.concat('元素1'，'元素2'，数组1)：将a数组的元素与参数中的元素（如果参数是数组，则提取这个数组中的所有元素），共同添加到新数组中；返回新数组



 */



/*
DOM：对HTML中所有内容作为对象进行操作
一.节点：网页中每一个部分都是一个节点，但是类型不一样
    -文档节点：整个html文档
    -元素节点：HTML文档中的HTML标签
    -属性节点:元素的属性
    -文本节点：HTML标签中的文本内容
    浏览器已经提供了文档节点对象-document，这个对象是window属性，可以在页面中直接使用


二.DOM操作
1.查找元素节点
  -document.getElementById:单个元素对象
  -getElementsByTagName/getElementsByName :返回一个类数组对象，将查询到的元素放入这个类数组中（即使查询到一个，也会放在类数组中）
2.读取元素属性(元素的属性可以在控制台element> properties查看)：
    -元素.属性名 ; 元素.innerHtml ;注意：元素.class不能采用这种方式，需要用元素.className
    -元素.属性.属性 ;元素.style.color

3.

三.事件:在事件对应的属性中，设置一些js代码；当事件触发，代码会执行；

1.为对应属性的对应事件绑定处理函数来响应事件
    -获取对象
        var logo=document.getElementById('banner_logo')
    -给对象绑定单击事件：给这个对象添加一个名为onclick,值为函数
        logo.onclick=function(){
            alert('click the logo')

        }
    -当logo对象触发click事件，那么函数执行






 */

var logo=document.getElementById("banner_logo");
var banner_title = document.getElementById("banner_title");


// setInterval(function(){ alert("Hello"); }, 3000);
// setInterval(function(){
//     banner_title.style.border = '1px solid red'; }, 2000);
//


/*
2.事件
(1)onload:在整个页面或者图片加载完成之后才触发
    window.onload=function(){
        alert('the page finish load')
    }








 */






/*
四.定时器

1.setInternal定时调用
















 */