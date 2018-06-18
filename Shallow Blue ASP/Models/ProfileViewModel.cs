using System;
using System.ComponentModel.DataAnnotations;

namespace Shallow_Blue_ASP.Models
{
    public class ProfileViewModel
    {
        [Required]
        [Display(Name = "User ID")]
        public int UserID { get; set; }

        [Required]
        [Display(Name = "First Name")]
        public string FirstName { get; set; }

        [Required]
        [Display(Name = "Last Name")]
        public string LastName { get; set; }

        [Required]
        [Display(Name = "Username")]
        public string Username { get; set; }
        
        [Required]
        [EmailAddress]
        [Display(Name = "Email Address")]
        public string Email { get; set; }

        [Required]
        [DataType(DataType.Date)]
        [Display(Name = "Date of Birth")]
        public DateTime DOB { get; set; }

        [Display(Name = "Chess Raiting")]
        public int Raiting { get; set; }

        [Required]
        [DataType(DataType.Password)]
        [Display(Name = "Current Password")]
        public string CurrentPassword { get; set; }
        
        [DataType(DataType.Password)]
        [Display(Name = "New Password")]
        public string NewPassword { get; set; }

        [DataType(DataType.Password)]
        [Compare("NewPassword", ErrorMessage = "The new passwords were different.")]
        [Display(Name = "Repeat New Password")]
        public string RepeatNewPassword { get; set; }
    }
}
