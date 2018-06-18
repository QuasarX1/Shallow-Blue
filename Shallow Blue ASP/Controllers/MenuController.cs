using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Shallow_Blue_ASP.Models;

namespace Shallow_Blue_ASP.Controllers
{
    public class MenuController : BaseController
    {
        [NonAction]
        new void AddTemplateData()
        {
            
        }

        /// <summary>
        /// Handles a request for the splash page.
        /// Site root page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult SplashPage()
        {
            ViewData["LoggedIn"] = TestLogin();
            ViewData["Admin"] = IsAdmin();

            AddTemplateData();
            return View();
        }

        /// <summary>
        /// Handles a request for the admin menu page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult AdminMenu()
        {
            AddTemplateData();
            return View();
        }

        /// <summary>
        /// Handles a GET request for the login page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        [HttpGet]
        public IActionResult Login()
        {
            return View();
        }

        /// <summary>
        /// Handles a POST request for the login page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        [HttpPost, ValidateAntiForgeryToken]
        public IActionResult Login(LoginModel model)
        {
            TempData["UserID"] = 1;
            TempData.Keep("UserID");

            TempData["Username"] = model.Username;
            TempData.Keep("Username");

            Flash("Hi " + TempData.Peek("Username"));

            return RedirectToAction("SplashPage");
        }

        /// <summary>
        /// Handles a request for the logout page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult Logout()
        {
            TempData.Remove("UserID");
            TempData.Remove("Username");

            return RedirectToAction("SplashPage");
        }

        /// <summary>
        /// Handles a request for the signup page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult Signup()
        {
            return View();
        }

        /// <summary>
        /// Handles a request for the ResetUserPassword page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult ResetUserPassword()
        {
            return View();
        }

        /// <summary>
        /// Handles a request for the DeleteUser page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult DeleteUser()
        {
            return View();
        }

        /// <summary>
        /// Handles a request for the BackupDatabase page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult BackupDatabase()
        {
            return View();
        }

        /// <summary>
        /// Handles a request for the Profiles page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult Profiles()
        {
            return View();
        }

        /// <summary>
        /// Handles a GET request for the Profile page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        [HttpGet]
        public IActionResult Profile()
        {
            var test = TempData["UserName"];

            return View(new ProfileViewModel
            {
                UserID = 1,
                FirstName = "Test",
                LastName = "User",
                Email = "Test@test.com",
                DOB = new DateTime(2000, 1, 1),
                Raiting = 1200                
            });
        }

        /// <summary>
        /// Handles a POST request for the Profile page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        [HttpPost, ValidateAntiForgeryToken]
        public IActionResult Profile(ProfileViewModel model)
        {

            return View(model);
        }

        /// <summary>
        /// Handles a request for the Watch page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult Watch()
        {

            return View("Join");
        }

        /// <summary>
        /// Handles a request for the Join page.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult Join()
        {

            return View();
        }

        /// <summary>
        /// Handles a n error in a request.
        /// </summary>
        /// <returns>Rendered view.</returns>
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}