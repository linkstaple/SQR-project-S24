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

function createCreateGroupClickHandler(ids) {
  return async () => {
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

    const createGroupResponse = await requestCreateGroup(groupName, memberIds)
    if (createGroupResponse.status === 403) {
      alert('Unauthorized request')
      return
    }
    if (createGroupResponse.status === 422) {
      alert('invalid list of members (list contains duplicates or empty)')
      return
    }
    if (createGroupResponse.status === 403) {
      alert('user in the member list not found')
      return
    }

    const {id: groupId} = await createGroupResponse.json()
    routeManager.goToGroup(groupId)
  }
}

async function requestCreateGroup(name, memberIds) {
  return makeRequest('/group', 'POST', {
    name,
    member_ids: memberIds
  })
}

async function profileScript() {
  const [profileResponse, groupsResponse, usersResponse] = await Promise.all([
    makeRequest('/profile', 'GET'),
    makeRequest(`/groups`, 'GET'),
    makeRequest(`/users`, 'GET')
  ])

  if (profileResponse.status === 403) {
    location.href = location.origin + '/login'
    return
  }

  const {username, id: userId} = await profileResponse.json()

  document.getElementsByTagName('title').item(0).textContent = username
  const usernameElem = document.getElementById('username')
  usernameElem.innerText = username

  const {groups} = await groupsResponse.json()

  const groupsListElem = document.getElementById('groups-list')
  const groupsItemsElements = groups.map(({id, name}) =>
    createGroupListElem(name, id)
  )

  groupsItemsElements.forEach(listElem => {
    groupsListElem.appendChild(listElem)
  })

  const {users: originalUsers} = await usersResponse.json()
  const users = originalUsers.filter(({id}) => id !== userId)

  const createGroupButton = document.getElementById('create-group-button')
  createGroupButton.onclick = createCreateGroupClickHandler(
    users.map(({id}) => id)
  )

  users.forEach(({username, id}) => addUserCheckbox(id, username))

  const logoutButton = document.getElementById('logout-button')
  logoutButton.onclick = () => authManager.logout()
}

profileScript()
