async function profileScript() {
  const profileResponse = await fetch("api/profile");
  const { username, id, token } = await profileResponse.json();

  document.getElementsByTagName("title").item(0).textContent = username;
  const usernameElem = document.getElementById("username");
  usernameElem.innerText = username;

  const groupsResponse = await fetch(`api/groups`, {
    method: 'GET',
    headers: { Authorization: token },
  });
  const { groups } = await groupsResponse.json();

  const groupsListElem = document.getElementById("groups-list");
  const groupsItemsElements = groups.map(({ name }) => {
    const listItem = document.createElement("li");
    listItem.textContent = name;
    return listItem;
  });

  groupsItemsElements.forEach((listElem) => {
    groupsListElem.appendChild(listElem);
  });
}

profileScript();
