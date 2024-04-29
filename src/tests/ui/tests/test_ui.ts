import {WebDriver, Builder, Browser, By, until} from 'selenium-webdriver'
import assert from 'assert'
import {Options} from 'selenium-webdriver/chrome'
import {
  Capabilities,
  UserPromptHandler
} from 'selenium-webdriver/lib/capabilities'
import {pages, users} from './helpers'

describe('LazySplit UI tests', () => {
  let driver: WebDriver
  let builder: Builder

  before(async () => {
    const chromeOptions = new Options()
    chromeOptions.setAlertBehavior(UserPromptHandler.ACCEPT)

    const chromeCapabilities = Capabilities.chrome()
    chromeCapabilities.setAlertBehavior(UserPromptHandler.ACCEPT)

    builder = new Builder()
    builder
      .setChromeOptions(chromeOptions)
      .withCapabilities(chromeCapabilities)
      .forBrowser(Browser.CHROME)
  })

  beforeEach(async () => {
    driver = await builder.build()

    await driver.manage().setTimeouts({
      implicit: 8000,
      pageLoad: 5000
    })
  })

  afterEach(async () => {
    driver.close()
  })

  describe('login & registration', () => {
    it('should load Login page for unauthorized user', async () => {
      await driver.get(pages.root)
      await driver.wait(
        until.urlMatches(/\/login/),
        5000,
        'Expecteed Login page to be opened for unauthorized user'
      )

      const actionButton = await driver.findElement(By.id('action-button'))
      const buttonText = await actionButton.getText()
      assert.equal(
        buttonText,
        'Register',
        'Expected button text to be "Register"'
      )
    })

    it('Register page should register', async () => {
      await driver.get(pages.register)

      const {name, password} = users.michael

      const loginInput = await driver.findElement(By.id('login-input'))
      await loginInput.sendKeys(name)

      const passwordInput = await driver.findElement(By.id('password-input'))
      await passwordInput.sendKeys(password)

      const submitButton = await driver.findElement(By.id('auth-submit-button'))
      await submitButton.click()

      await driver.wait(
        until.urlContains('profile'),
        7000,
        'Profile page is not opened'
      )

      const logoutButton = await driver.findElement(By.id('logout-button'))
      await logoutButton.click()
    })

    it('check for empty login credentials', async () => {
      await driver.get(pages.login)
      const {name, password} = users.andrew

      const submitButton = await driver.findElement(By.id('auth-submit-button'))
      await submitButton.click()

      driver.wait(until.alertIsPresent(), 4000, 'Expected alert to be shown')
      let alert = await driver.switchTo().alert()
      let alertText = await alert.getText()
      assert.match(
        alertText,
        /login\sis\snot\sspecified/,
        'Alert for non-specified username is not shown'
      )

      await alert.accept()

      const loginInput = await driver.findElement(By.id('login-input'))
      await loginInput.sendKeys(name)

      await submitButton.click()

      alert = await driver.switchTo().alert()
      alertText = await alert.getText()
      assert.match(
        alertText,
        /Password\sis\snot\sspecified/,
        'Alert for non-specified password is not shown'
      )
      await alert.accept()

      const passwordInput = await driver.findElement(By.id('password-input'))
      await passwordInput.sendKeys(password)

      await submitButton.click()

      alert = await driver.switchTo().alert()
      alertText = await alert.getText()
      assert.match(
        alertText,
        /Invalid\susername\sor\spassword/,
        'Alert for non-existing user is not shown'
      )
    })

    it('should login user', async () => {
      await driver.get(pages.login)
      const {name, password} = users.michael

      const loginInput = await driver.findElement(By.id('login-input'))
      await loginInput.sendKeys(name)

      const passwordInput = await driver.findElement(By.id('password-input'))
      await passwordInput.sendKeys(password)

      const submitButton = await driver.findElement(By.id('auth-submit-button'))
      await submitButton.click()

      await driver.wait(
        until.urlContains('profile'),
        7000,
        'Profile page is not opened'
      )

      const logoutButton = await driver.findElement(By.id('logout-button'))
      await logoutButton.click()
    })
  })

  describe('profile page', () => {
    it('should create group', async () => {
      // register user Andrew
      await driver.get(pages.register)

      const {andrew, timur} = users

      let loginInput = await driver.findElement(By.id('login-input'))
      await loginInput.sendKeys(andrew.name)

      let passwordInput = await driver.findElement(By.id('password-input'))
      await passwordInput.sendKeys(andrew.password)

      let submitButton = await driver.findElement(By.id('auth-submit-button'))
      await submitButton.click()

      await driver.wait(
        until.urlContains('profile'),
        7000,
        'Profile page is not opened'
      )

      // register user Timur
      const logoutButton = await driver.findElement(By.id('logout-button'))
      await logoutButton.click()

      await driver.get(pages.register)

      loginInput = await driver.findElement(By.id('login-input'))
      await loginInput.sendKeys(timur.name)

      passwordInput = await driver.findElement(By.id('password-input'))
      await passwordInput.sendKeys(timur.password)

      submitButton = await driver.findElement(By.id('auth-submit-button'))
      await submitButton.click()

      await driver.wait(
        until.urlContains('profile'),
        7000,
        'Profile page is not opened'
      )

      // creating new group
      const checkboxes = await driver.findElements(By.css('[type=checkbox]'))
      await Promise.all(checkboxes.map(async checkbox => checkbox.click()))

      const groupNameInput = await driver.findElement(By.id('group-name-input'))
      groupNameInput.sendKeys('abrakadabra')

      const createGroupButton = await driver.findElement(
        By.id('create-group-button')
      )
      await createGroupButton.click()

      await driver.wait(
        until.urlMatches(/group\/\d/),
        7000,
        'Expected URL to change to /group/:group_id'
      )
    })

    it('should show create group alerts', async () => {
      // login and open profile
      await driver.get(pages.login)
      const {michael} = users

      const loginInput = await driver.findElement(By.id('login-input'))
      await loginInput.sendKeys(michael.name)

      const passwordInput = await driver.findElement(By.id('password-input'))
      await passwordInput.sendKeys(michael.password)

      const submitButton = await driver.findElement(By.id('auth-submit-button'))
      await submitButton.click()

      await driver.wait(
        until.urlContains('profile'),
        7000,
        'Profile page is not opened'
      )

      // trying to create a new group
      const createGroupButton = await driver.findElement(
        By.id('create-group-button')
      )
      await createGroupButton.click()

      await driver.wait(until.alertIsPresent(), 1000, 'Alert is not shown')
      let alert = await driver.switchTo().alert()

      let alertText = await alert.getText()
      assert.match(
        alertText,
        /choose at least 1 member/,
        'Alert about choosing at least 1 member is not shown'
      )
      alert.accept()

      const checkboxes = await driver.findElements(By.css('[type=checkbox]'))
      assert.equal(
        checkboxes.length > 0,
        true,
        'Expected to have at least 1 checkbox for users'
      )

      const checkboxElem = checkboxes[0]
      checkboxElem.click()
      createGroupButton.click()

      await driver.wait(until.alertIsPresent(), 1000, 'Alert is not shown')
      alert = await driver.switchTo().alert()
      alertText = await alert.getText()
      assert.match(
        alertText,
        /Group name is not specified/,
        'Expected alert about empty group name'
      )
    })
  })
})
