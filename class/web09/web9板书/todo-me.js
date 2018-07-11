/*
打印调试
*/
var log = function() {
    console.log.apply(console, arguments)
}

/*
封装的选择器函数
 */
var e = function (sel) {
    log('e 正常')
    return document.querySelector(sel)
}

/*
封装插入的HTML文本
 */
var todoTemplate = function (todo) {
    var t = `
        <div class="todo-cell">
            <button class="todo-delete">delete</button>
            <span>${todo}</span>
        </div>
    `
    log('todoTemplate 正常')
    return t
}

/*
将HTML文本插入
 */
var insertTodo = function(todo) {
    var todoCell = todoTemplate(todo)
    log(todoCell)
    var todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
    log('insertTodo正常')
}

var b = e('#id-button-add')

b.addEventListener('click', function () {
    log('click')
    var input = e('#id-input-todo')
    var todo = input.value
    log('todo', todo)
    insertTodo(todo)
    log('addEventListener正常')
})

var todoList = e('.todo-list')

todoList.addEventListener('click', function (event) {
    log('add')
    var self = event.target
    if (self.classList.contains('todo-delete')) {
        log('点到了删除按钮')
        self.parentElement.remove()
    } else {

    }
})