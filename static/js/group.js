function requestSplit(groupId, amount, landerId, payers) {
  return makeRequest('/split', 'POST', {
    group_id: groupId,
    amount,
    lander_id: landerId,
    payer_ids: payers
  })
}

function getUsernameById(members, userId) {
  return members.find(({id}) => id === userId).username
}

function requestGroupData() {
  const groupId = Number(new URL(location.href).pathname.split('/')[2])
  return makeRequest(`/group/${groupId}`, 'GET')
}

function populateMembersList(members) {
  const membersListElem = document.getElementById('members-list')
  members.forEach(({username, balance}) => {
    const listItemElem = document.createElement('li')
    listItemElem.className = 'member-list-item'

    const usernameDiv = document.createElement('div')
    usernameDiv.textContent = username

    const deptDiv = document.createElement('div')
    deptDiv.textContent = `balance: ${balance.toFixed(2)}`
    deptDiv.style.marginTop = '5px'

    listItemElem.appendChild(usernameDiv)
    listItemElem.appendChild(deptDiv)

    membersListElem.appendChild(listItemElem)
  })
}

function populateGroupTitle(title) {
  const titleElem = document.getElementById('group-title')
  titleElem.textContent = title
}

function populateLanderSelect(members) {
  const selectElem = document.getElementById('lander-select')
  members.forEach(({id, username}) => {
    const optionElem = document.createElement('option')
    optionElem.value = id
    optionElem.textContent = username
    selectElem.appendChild(optionElem)
  })
}

function populatePayersFieldset(members) {
  const fieldsetElem = document.getElementById('payers-fieldset')
  members.forEach(({id, username}) => {
    const elemId = `select_payer_${id}`

    const inputElem = document.createElement('input')
    inputElem.type = 'checkbox'
    inputElem.id = elemId

    const labelElem = document.createElement('label')
    labelElem.style.marginLeft = '5px'
    labelElem.for = elemId
    labelElem.textContent = username

    const div = document.createElement('div')
    div.appendChild(inputElem)
    div.appendChild(labelElem)

    fieldsetElem.appendChild(div)
  })
}

function populateHistory(history, members) {
  const historyListElem = document
    .getElementsByClassName('history-list')
    .item(0)
  history.forEach(({timestamp, amount, doer_id, lander_id, payer_ids}) => {
    const listItem = document.createElement('li')
    listItem.className = 'history-item'

    const timestampDiv = document.createElement('div')
    timestampDiv.textContent = `Date: ${new Date(
      timestamp * 1000
    ).toLocaleString()}`

    const amountDiv = document.createElement('div')
    amountDiv.textContent = `Amount: ${amount.toFixed(2)}`
    amountDiv.style.marginTop = '5px'

    const landerDiv = document.createElement('div')
    landerDiv.textContent = `Lander: ${getUsernameById(members, lander_id)}`
    landerDiv.style.marginTop = '5px'

    const doerDiv = document.createElement('div')
    doerDiv.textContent = `Doer: ${getUsernameById(members, doer_id)}`
    doerDiv.style.marginTop = '5px'

    const payersDiv = document.createElement('div')
    const payersText = payer_ids
      .map(id => getUsernameById(members, id))
      .join(', ')
    payersDiv.textContent = `Payers: ${payersText}`
    payersDiv.style.marginTop = '5px'

    listItem.appendChild(timestampDiv)
    listItem.appendChild(amountDiv)
    listItem.appendChild(landerDiv)
    listItem.appendChild(doerDiv)
    listItem.appendChild(payersDiv)

    historyListElem.appendChild(listItem)
  })
}

function createSplitHandler(members, groupId) {
  return async () => {
    const landerId = document.getElementById('lander-select').value
    if (!landerId) {
      alert('Lander is not specified')
      return
    }

    const payersIds = members
      .map(({id}) => id)
      .filter(id => document.getElementById(`select_payer_${id}`).checked)

    if (payersIds.length === 0) {
      alert('You should choose at least 1 payer')
      return
    }

    const amount = document.getElementById('amount-input').value
    if (!amount) {
      alert('Amount is not specified')
      return
    }

    const splitResponse = await requestSplit(
      groupId,
      amount,
      landerId,
      payersIds
    )
    if (!splitResponse.ok) {
      const msg = await splitResponse.json()
      alert(msg)
      return
    }
    window.location.reload()
  }
}

async function groupScript() {
  const groupResponse = await requestGroupData()
  if (groupResponse.status === 403) {
    routeManager.goToLogin()
    return
  }

  if (groupResponse.status === 404) {
    routeManager.goToProfile()
    return
  }

  const {
    id: groupId,
    name: groupName,
    members,
    history
  } = await groupResponse.json()

  populateGroupTitle(groupName)
  populateMembersList(members)
  populateLanderSelect(members)
  populatePayersFieldset(members)
  populateHistory(history, members)

  const splitButtonElem = document.getElementById('split-money-button')
  splitButtonElem.onclick = createSplitHandler(members, groupId)

  const goBackButton = document.getElementById('go-to-profile-button')
  goBackButton.onclick = routeManager.goToProfile
}

groupScript()
