using System;
using System.ComponentModel.DataAnnotations;

namespace Shallow_Blue_ASP.Models
{
    public class LoginModel
    {
        [Required]
        public string UserName { get; set; }

        //[Required]
        //[EmailAddress]
        //[Display(Name = "Email Address")]
        //public string Email { get; set; }

        [Required]
        [DataType(DataType.Password)]
        public string Password { get; set; }
    }
}
