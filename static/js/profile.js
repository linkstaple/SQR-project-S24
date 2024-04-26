function createGroupListElem(name, id) {
  const elem = document.createElement('li')
  elem.className = 'group-list-item'
  elem.textContent = name

  elem.onclick = () => {
    location.href = location.origin + `/group/${id}`
  }
  return elem
}

function addUserCheckbox(id, name) {
  const elemId = `add_user_${id}`

  const inputElem = document.createElement('input')
  inputElem.type = 'checkbox'
  inputElem.id = elemId

  const labelElem = document.createElement('label')
  labelElem.style.marginLeft = '5px'
  labelElem.for = elemId
  labelElem.textContent = name

  const div = document.createElement('div')
  div.appendChild(inputElem)
  div.appendChild(labelElem)

  const fieldsetElem = document.getElementById('fieldset')
  fieldsetElem.appendChild(div)
}

function createClickCreateGroupHandler(ids) {
  return () => {
    const memberIds = ids.filter(
      id => document.getElementById(`add_user_${id}`).checked
    )

    if (memberIds.length === 0) {
      alert('You must choose at least 1 member')
      return
    }

    const groupName = document.getElementById('group-name-input').value
    if (!groupName) {
      alert('Group name is not specified')
      return
    }
    requestCreateGroup(groupName, memberIds)
  }
}

async function requestCreateGroup(name, memberIds) {
  return fetch('/api/group', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name,
      member_ids: memberIds
    })
  })
}

async function profileScript() {
  // const [profileResponse, groupsResponse] = await Promise.all([
  //   fetch("api/profile", {
  //     method: "GET",
  //     headers: { Authorization: token },
  //   }),
  //   fetch(`api/groups`, {
  //     method: "GET",
  //     headers: { Authorization: token },
  //   }),
  // ]);

  // if (profileResponse.status === 403) {
  //   location.href = location.origin + "/login";
  //   return;
  // }
  // const { username, id, token } = await profileResponse.json();
  const createGroupButton = document.getElementById('create-group-button')
  username = 'Michael'

  document.getElementsByTagName('title').item(0).textContent = username
  const usernameElem = document.getElementById('username')
  usernameElem.innerText = username

  // const { groups } = await groupsResponse.json();
  groups = [
    {name: 'dengovie', id: 1},
    {name: 'poga', id: 2},
    {name: 'fanaty_serdyuchki', id: 3}
  ]

  const groupsListElem = document.getElementById('groups-list')
  const groupsItemsElements = groups.map(({id, name}) =>
    createGroupListElem(name, id)
  )

  groupsItemsElements.forEach(listElem => {
    groupsListElem.appendChild(listElem)
  })

  const users = [
    {name: 'michael', id: 1},
    {name: 'andrew', id: 2},
    {name: 'timur', id: 3}
  ]

  createGroupButton.onclick = createClickCreateGroupHandler(
    users.map(({id}) => id)
  )

  users.forEach(({name, id}) => addUserCheckbox(id, name))
}

profileScript()
