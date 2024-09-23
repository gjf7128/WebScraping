import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;

class TigerCenterClass {
    private static final Browser BROWSER
            = Browser.CHROME; // Can be changed to Browser.CHROME

    private WebDriver driver;

    @BeforeAll
    static void setUpAll() {
        System.err.println("Will try WebDriver at path:");
        System.err.println(Browser.getWebDriverPathFor(BROWSER));
    }

    @BeforeEach
    void setUp() {
        driver = BROWSER.setUpWebDriver();
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(30));
    }

    @AfterEach
    void tearDown() {
        driver.quit();
    }

    @Test
    void testClassSearchButton() throws Exception {
        driver.get("https://tigercenter.rit.edu/");
        WebElement classButton = driver.findElement(By.xpath("//*[@id=\"angularApp\"]/app-root/div[2]/mat-sidenav-container[2]/mat-sidenav-content/div[2]/landing-page/div/div/div/div/div[4]/a[1]"));
        assertEquals("Class Search", classButton.getText());
        classButton.click();
        Thread.sleep(1000);
    }

    //Test by Gabriel FitzPatrick, gjf7128
    @Test
    void testDisplayTigerCenterResults() throws InterruptedException {
        List<WebElement> elements;
        WebDriver driver = new ChromeDriver();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        driver.get("https://tigercenter.rit.edu/");
        wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//*[@id=\"angularApp\"]/app-root/div[2]/mat-sidenav-container[2]/mat-sidenav-content/div[2]/landing-page/div/div/div/div/div[4]/a[1]"))).click();
        //Successfully got to class search page
        wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//*[@id=\"hideTerm\"]/div/select/option[2]"))).click();
        //Successfully waited for page to load and selected desired term.
        WebElement textField = wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//*[@id=\"ng2Completer\"]/div/input")));
        textField.sendKeys("CSEC");
        driver.findElement(By.xpath("//*[@id=\"classSearchContainer\"]/div[2]/form/div/button")).click();
        // I would use wait.until... but i'm pretty sure the element containing results is already clickable before
        // even entering a search and so we're waiting 3 seconds here just incase.
        Thread.sleep(3000);

        //We Are getting the whole element holding results and then filtering by only the rows, leaving out the header
        WebElement resultsContainer = driver.findElement(By.xpath("//*[@id=\"classSearchContainer\"]/div[2]/div[4]/div[5]"));
        elements = resultsContainer.findElements(By.tagName("app-class-search-row"));
        System.out.println("Search Results:\n");
        for (WebElement element : elements) {
            //We are forced to parse strings because WebElements have no way to be uniquely found with classNames,
            //tagNames, etc.  I tried.
            String elementText = element.getText();
            String[] elementTextSplit = elementText.split("\\r?\\n");
            System.out.println("Course Name: " + elementTextSplit[0]);
            System.out.println("Days/Times: " + elementTextSplit[7]);
            System.out.println("Location: " + elementTextSplit[9]);
            System.out.println("Instructor: " + elementTextSplit[10] + "\n");
        }
    }

    private enum Browser {
        CHROME("webdriver.chrome.driver",
                "chromedriver",
                ChromeDriver::new),
        FIREFOX("webdriver.gecko.driver",
                "geckodriver",
                FirefoxDriver::new);

        private final String driverPropertyKey;
        private final String driverBaseName;
        private final Supplier<WebDriver> webDriverSupplier;

        Browser(String driverPropertyKey,
                String driverBaseName,
                Supplier<WebDriver> webDriverSupplier) {
            this.driverPropertyKey = driverPropertyKey;
            this.driverBaseName = driverBaseName;
            this.webDriverSupplier = webDriverSupplier;
        }

        private static Path getWebDriverPathFor(Browser browser) {
            String driverFileName = browser.driverBaseName;
            if (System.getProperty("os.name").startsWith("Windows")) {
                driverFileName += ".exe";
            }
            return Paths.get(System.getProperty("user.dir"), driverFileName);
        }

        private WebDriver setUpWebDriver() {
            Path driverPath = getWebDriverPathFor(this);
            System.setProperty(this.driverPropertyKey, driverPath.toString());
            return this.webDriverSupplier.get();
        }
    }
}