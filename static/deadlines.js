// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  const daysLeft = opportunity.days_left;
  let text = "";
  let colour = "";

  // Pass or Fail: a deadline that has passed fails, today or later passes.
  // (With today = 3 Nov, 2 Nov and earlier fail, 3 Nov and later pass.)
  const result = document.createElement("div");
  if (daysLeft < 0) {
    result.className = "deadline-label deadline-fail";
    result.textContent = "Fail";
  } else {
    result.className = "deadline-label deadline-pass";
    result.textContent = "Pass";
  }
  cell.appendChild(result);

  if (daysLeft < 0) {
    text = "Overdue";
    colour = "red";
  } else if (daysLeft === 0) {
    text = "Due today";
    colour = "yellow";
  } else if (daysLeft <= 7) {
    text = daysLeft === 1 ? "Due in 1 day" : "Due in " + daysLeft + " days";
    colour = "yellow";
  }

  // More than 7 days away: show the date only.
  if (text === "") {
    return;
  }

  const label = document.createElement("div");
  label.className = "deadline-label deadline-" + colour;
  label.textContent = text;
  cell.appendChild(label);
}
