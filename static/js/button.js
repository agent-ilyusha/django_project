function addRecordField() {
    let x = document.getElementsByClassName("main_div_sr").length;
    const str =
        '<h4>Запись ' + (x + 1) + '</h4><label for="type_work">Тип работы</label>' +
        '<input id="sr_type_work" name="type_work' + x + '" type="text"><br>' +
        '<label for="the_date_of_the">Дата проведения работ</label>' +
        '<input id="sr_the_date_of_the" name="the_date_of_the' + x + '" type="date"><br>' +
        '<label for="price">Цена</label>' +
        '<input id="sr_price" name="price' + x + '" type="number">';

    let doc = document.getElementById('service_main_div');
    let div = document.createElement('div');
    div.id = x;
    div.setAttribute("class", "main_div_sr");
    doc.appendChild(div);
    div.innerHTML = str;
}


function delRecordField() {
    let div = document.getElementById('service_main_div');
    if (x > 0){
        const child = div.childNodes[div.childNodes.length-1];
        div.removeChild(child);
    }

}

function date_iso(date) {
    return date.reverse()
}
