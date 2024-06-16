const high_block = document.getElementById("high_block"); // получение элем по айди

fetch("/get_schedule") // фетч запрос по эндпоинту get_schedule, чтоб получить расписание врачей
  .then((response) => {
    return response.json(); // парсинг ответа из json
  })
  .then((data) => {
    for (let i = 0; data.length > i; i++) {
      // пробегаемся по длине всех расписаний каждого доктора
      doc_info = data[i]; // информация по одному данному доктору
      const name_ = document.createElement("p"); // создание тега под имя доктора
      name_.innerText = doc_info[1]; // вставка имени доктора в тег для него
      name_.className += "name"; // добавление класса для тега для доктора, чтоб добавить стили к нему
      high_block.appendChild(name_); // добавление самого тега в существующий на странице блок, чтоб было видно информацию
      let count = 0; // счетчик дней
      let currentDate = new Date(); // для указания точной текущей даты при расписании
      const forSchedule = document.createElement("div"); // блок для полного расписания КАЖДОГО врача
      forSchedule.className += "forSchedule"; // добавление класса блоку
      high_block.appendChild(forSchedule); // добавление блока на страницу
      for (let d of doc_info.slice(2)) {
        // бежим по информации о докторе, пропуская первые два значения, ввиду айди, имени
        count += 1; // плюсуем день
        const schedule_block = document.createElement("div"); // cоздаем блок для расписания
        schedule_block.className += "schedule_block"; // добавление класса для тега для расписания, чтоб добавить стили к нему
        const schedule = document.createElement("p"); // создаем тег p для хранения непосредственно расписания
        schedule.innerHTML = `${count}/${currentDate.getMonth()}/${currentDate.getFullYear()} </br> ${d}`; // вставка дней, для которых расписание
        schedule.className += "schedule"; // добавление класса для тега для расписания
        schedule_block.appendChild(schedule); // добавление расписания в блок для него
        forSchedule.appendChild(schedule_block); // добавление блока в основной блок на странице
        if (d === null) {
          // дни, которые доктор не работает содержат нулл, что обозначает выходной
          schedule.innerHTML = `${count}/${currentDate.getMonth()}/${currentDate.getFullYear()} </br> выходной`; // обозначаем выходной
        }
      }
    }
  });
