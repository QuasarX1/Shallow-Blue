using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace Shallow_Blue_ASP.Controllers
{
    public static class Operations
    {
        public static Dictionary<string, dynamic> addTemplateData()
        {
            Dictionary<string, dynamic> data = new Dictionary<string, dynamic>();

            data["Messages"] = new List<string>();

            return data;
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
