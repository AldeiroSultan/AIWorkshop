// This runs once for every row in the table.
//   row          the table row (<tr>)
//   cell         the deadline cell (<td>)
//   opportunity  the row's data, including days_left from the server
function showDeadline(row, cell, opportunity) {
  const daysLeft = opportunity.days_left;

  let label = null;
  let className = null;

  if (daysLeft < 0) {
    label = "Overdue";
    className = "deadline-overdue";
  } else if (daysLeft === 0) {
    label = "Due today";
    className = "deadline-today";
  } else if (daysLeft <= 7) {
    label = "Due in " + daysLeft + " day" + (daysLeft === 1 ? "" : "s");
    className = "deadline-soon";
  }

  if (label) {
    cell.classList.add(className);
    const badge = document.createElement("span");
    badge.className = "deadline-label " + className;
    badge.textContent = label;
    cell.appendChild(badge);
  }
}
