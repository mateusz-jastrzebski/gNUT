function updateUpsList() {
        $.getJSON('/get_ups_list', function(dict) {
            let data = dict.ups_list;

            let table = document.getElementById("ups_table").getElementsByTagName('tbody')[0];
            for (const element of table.rows) {
                let row = element;

                const name = row.cells[0];
                const upsName = name.innerText;

                const description = row.cells[1];
                const status = row.cells[2];
                const batterylow = row.cells[3];
                const battery = row.cells[4];
                const load = row.cells[5];


                name.children[0].children[0].innerHTML = data[upsName].ups;
                description.innerHTML = data[upsName].description;
                status.innerHTML = data[upsName].status;
                batterylow.innerHTML = data[upsName].batterylow+"%";
                battery.innerHTML = `<progress id="${upsName}_bat" value="${data[upsName].battery}" max="100">${data[upsName].battery}% </progress> ${data[upsName].battery}%</td>`;
                load.innerHTML = `<progress id="${upsName}_load" value="${data[upsName].load}" max="100">${data[upsName].load}% </progress> ${data[upsName].load}%</td>`;

            }
        });
}

let intervalId;

function startInterval() {
    intervalId = setInterval(updateUpsList, 3000);
}

function stopInterval() {
  clearInterval(intervalId);
}

startInterval();