import {
  WebDriver,
  Builder,
  Browser,
  By,
  until
} from 'selenium-webdriver'
import assert from 'assert'
import {Options} from 'selenium-webdriver/chrome'
import {
  Capabilities,
  UserPromptHandler
} from 'selenium-webdriver/lib/capabilities'

describe('UI tests', () => {
  let driver: WebDriver

  before(async () => {})

  beforeEach(async () => {
    const chromeOptions = new Options()
    chromeOptions.setAlertBehavior(UserPromptHandler.ACCEPT)
    const chromeCapabilities = Capabilities.chrome().setAlertBehavior(
      UserPromptHandler.ACCEPT
    )
    const builder = new Builder()

    builder.setChromeOptions(chromeOptions)

    driver = await builder
      .withCapabilities(chromeCapabilities)
      .forBrowser(Browser.CHROME)
      .build()

    await driver.manage().setTimeouts({
      implicit: 3000
    })
  })

  afterEach(async () => {
    driver.close()
  })

  it('should load Login page for unauthorized user', async () => {
    await driver.get('http://127.0.0.1:8000/')
    const actionButton = await driver.findElement(By.id('action-button'))

    const url = await driver.getCurrentUrl()
    assert.match(url, /\/login/, 'Expected login page to be opened')

    const buttonText = await actionButton.getText()
    assert.equal(
      buttonText,
      'Register',
      'Expected button text to be "Register"'
    )
  })

  it('Register page should register', async () => {
    await driver.get('http://127.0.0.1:8000/register')

    const loginInput = await driver.findElement(By.id('login-input'))
    await loginInput.sendKeys('michael')

    const passwordInput = await driver.findElement(By.id('password-input'))
    await passwordInput.sendKeys('1')

    const submitButton = await driver.findElement(By.id('auth-submit-button'))
    await submitButton.click()

    await driver.wait(
      until.urlContains('profile'),
      2000,
      'Profile page is not opened'
    )

    const logoutButton = await driver.findElement(By.id('logout-button'))
    await logoutButton.click()
  })

  it('check for empty login credentials', async () => {
    await driver.get('http://127.0.0.1:8000/login')

    const submitButton = await driver.findElement(By.id('auth-submit-button'))
    await submitButton.click()

    driver.wait(until.alertIsPresent(), 1000, 'Expected alert to be shown')
    let alert = await driver.switchTo().alert()
    let alertText = await alert.getText()
    assert.match(
      alertText,
      /login\sis\snot\sspecified/,
      'Alert for non-specified username is not shown'
    )

    await alert.accept()

    const loginInput = await driver.findElement(By.id('login-input'))
    await loginInput.sendKeys('andrew')

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
    await passwordInput.sendKeys('2')

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
    await driver.get('http://127.0.0.1:8000/login')

    const loginInput = await driver.findElement(By.id('login-input'))
    await loginInput.sendKeys('michael')

    const passwordInput = await driver.findElement(By.id('password-input'))
    await passwordInput.sendKeys('1')

    const submitButton = await driver.findElement(By.id('auth-submit-button'))
    await submitButton.click()

    await driver.wait(
      until.urlContains('profile'),
      2000,
      'Profile page is not opened'
    )
  })
})
