using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Shallow_Blue_ASP.Models;
using static Shallow_Blue_ASP.Controllers.Operations;

namespace Shallow_Blue_ASP.Controllers
{
    public class MenuController : Controller
    {
        private void addTemplateData()
        {
            foreach (KeyValuePair<string, dynamic> item in Operations.addTemplateData())
            {
                ViewData[item.Key] = item.Value;
            }
            
        }

        public IActionResult SplashPage()
        {
            ViewData["LoggedIn"] = TestLogin();
            ViewData["Admin"] = IsAdmin();

            addTemplateData();
            return View();
        }

        public IActionResult About()
        {
            ViewData["Message"] = "Your application description page.";

            return View();
        }

        public IActionResult Contact()
        {
            ViewData["Message"] = "Your contact page.";

            return View();
        }

        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
