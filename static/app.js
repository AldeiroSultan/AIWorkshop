// Loads the opportunities from the API and shows them in the table.
async function renderTable() {
  const response = await fetch("/api/opportunities");
  const opportunities = await response.json();

  const tbody = document.getElementById("opportunity-rows");
  tbody.innerHTML = "";

  for (const opportunity of opportunities) {
    const row = document.createElement("tr");

    const nameCell = addCell(row, "");
    const name = document.createElement(opportunity.link ? "a" : "span");
    name.className = "name";
    name.textContent = opportunity.name;
    if (opportunity.link) {
      name.href = opportunity.link;
      name.target = "_blank";
    }
    nameCell.appendChild(name);
    const organization = document.createElement("div");
    organization.className = "organization";
    organization.textContent = opportunity.organization;
    nameCell.appendChild(organization);

    const deadlineCell = addCell(row, formatDate(opportunity.deadline));
    showDeadline(row, deadlineCell, opportunity); // in deadlines.js

    const ownerCell = addCell(row, "");
    const avatar = document.createElement("span");
    avatar.className = "avatar";
    avatar.textContent = opportunity.owner.charAt(0);
    ownerCell.append(avatar, opportunity.owner);

    const statusCell = addCell(row, "");
    const badge = document.createElement("span");
    badge.className = "status status-" + opportunity.status.toLowerCase();
    badge.textContent = opportunity.status;
    statusCell.appendChild(badge);

    addCell(row, formatAmount(opportunity.amount));
    addCell(row, opportunity.next_step);

    tbody.appendChild(row);
  }
}

// Adds a table cell with plain text. textContent keeps user input safe.
function addCell(row, text) {
  const cell = document.createElement("td");
  cell.textContent = text;
  row.appendChild(cell);
  return cell;
}

// Turns "2026-11-15" into "Nov 15, 2026".
function formatDate(isoDate) {
  const [year, month, day] = isoDate.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

// Turns 5000 into "C$5,000". Unknown amounts show a dash.
function formatAmount(amount) {
  if (amount === null) {
    return "—";
  }
  return "C$" + amount.toLocaleString("en-CA");
}

renderTable();
