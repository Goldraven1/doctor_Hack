fetch("/get_schedule")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log(data);
  });
