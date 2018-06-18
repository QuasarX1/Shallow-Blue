using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Shallow_Blue_ASP.Models;

namespace Shallow_Blue_ASP.Controllers
{
    public class BaseController : Controller
    {
        /// <summary>
        /// Method for adding data that is required by the template.
        /// Must be overriden in each controller definition.
        /// </summary>
        [NonAction]
        protected void AddTemplateData()
        {
            throw new NotImplementedException("This method must be overridden in the controller.");
        }

        /// <summary>
        /// Adds a message to TempData
        /// </summary>
        /// <param name="message"></param>
        [NonAction]
        protected void Flash(string message)
        {
            string key = "Message " + DateTime.Now.ToString();
            TempData[key] = message;
            TempData.Keep(key);
        }

        public static bool TestLogin()
        {
            return false;
        }

        public static bool IsAdmin()
        {
            return false;
        }
    }
}
