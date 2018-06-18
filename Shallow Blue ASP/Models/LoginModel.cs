using System;
using System.ComponentModel.DataAnnotations;

namespace Shallow_Blue_ASP.Models
{
    public class LoginModel
    {
        [Required]
        [Display(Name = "Username")]
        public string Username { get; set; }
        
        [Required]
        [DataType(DataType.Password)]
        [Display(Name = "Password")]
        public string Password { get; set; }

        //[Required]
        //[EmailAddress]
        //[Display(Name = "Email Address")]
        //public string Email { get; set; }
    }
}
