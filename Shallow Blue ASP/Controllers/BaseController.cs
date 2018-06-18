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

        protected bool TestLogin()
        {
            if (TempData["UserID"] == null)
            {
                return false;
            }
            else
            {
                return true;
            }
        }

        protected bool IsAdmin()
        {
            if ((string)TempData["UserName"] == "admin")
            {
                return true;
            }
            else
            {
                return false;
            }
        }
    }
}
